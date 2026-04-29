/* selfOS Knowledge Graph — Canvas Renderer with Glow Effects + View Presets */

(function () {
    "use strict";

    // ── Type Colors ──

    var TYPE_COLORS = {
        "concept":       "#4a9eff",
        "entity-person": "#f59e0b",
        "entity-org":    "#34d399",
        "entity-tool":   "#a78bfa",
        "synthesis":     "#facc15"
    };

    var TYPE_LABELS = {
        "concept":       "Concept",
        "entity-person": "Person",
        "entity-org":    "Org",
        "entity-tool":   "Tool",
        "synthesis":     "Synthesis"
    };

    // ── Tag Cluster Palette ──

    var TAG_PALETTE = [
        "#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4",
        "#feca57", "#ff9ff3", "#54a0ff", "#5f27cd"
    ];
    var TAG_DEFAULT_COLOR = "#555";

    // ── State ──

    var rawData = null;
    var nodes = [];
    var edges = [];
    var nodeMap = {};
    var adjacency = {};      // nodeId -> [{edgeIdx, otherId}]
    var hiddenTypes = {};
    var selectedNodeId = null;
    var hoveredNodeId = null;
    var dragNode = null;
    var physicsStopped = false;
    var stabilizationCount = 0;
    var STABILIZATION_THRESHOLD = 300;

    // Camera
    var camera = { x: 0, y: 0, zoom: 1 };
    var isPanning = false;
    var panStart = { x: 0, y: 0 };
    var panCameraStart = { x: 0, y: 0 };

    // Animation
    var breathPhase = 0;
    var pulsePhase = 0;
    var animFrame = null;
    var lastTime = 0;

    // Fade animation for filters
    var nodeOpacities = {};  // nodeId -> {current, target}

    // ── Color Transition State ──

    var nodeColors = {};      // nodeId -> {r, g, b, targetR, targetG, targetB}
    var COLOR_LERP_SPEED = 0.06; // per frame, ~300ms to settle

    // ── Preset State ──

    var currentPreset = "type";
    var presetDropdownOpen = false;

    // Computed preset metadata (built after data loads)
    var tagColorMap = {};     // tag -> color hex
    var topTags = [];         // ordered list of top N tags
    var dateRange = { min: null, max: null }; // Date objects
    var degreeRange = { min: 0, max: 0 };
    var sourceRange = { min: 0, max: 0 };

    // ── DOM refs ──

    var container = document.getElementById("graph-container");
    var canvas = document.getElementById("graph-canvas");
    var ctx = canvas.getContext("2d");
    var detailPanel = document.getElementById("detail-panel");
    var searchBox = document.getElementById("search-box");
    var statsEl = document.querySelector("#header .stats");
    var loadingOverlay = document.querySelector(".loading-overlay");
    var filterButtons = document.querySelectorAll(".filter-btn");
    var presetBtn = document.getElementById("preset-btn");
    var presetLabel = document.getElementById("preset-label");
    var presetDropdown = document.getElementById("preset-dropdown");
    var presetOptions = document.querySelectorAll(".preset-option");
    var legendEl = document.getElementById("graph-legend");

    // ── Canvas sizing ──

    function resizeCanvas() {
        var dpr = window.devicePixelRatio || 1;
        var rect = container.getBoundingClientRect();
        canvas.width = rect.width * dpr;
        canvas.height = rect.height * dpr;
        canvas.style.width = rect.width + "px";
        canvas.style.height = rect.height + "px";
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    // ── Init ──

    fetch("/api/graph")
        .then(function (res) { return res.json(); })
        .then(function (data) {
            rawData = data;
            buildGraph(data);
            computePresetMetadata();
            applyPreset("type");
            hideLoading();
            startAnimation();
            updateLegend();
        })
        .catch(function () {
            loadingOverlay.textContent = "Failed to load graph.";
        });

    // ── Build Graph ──

    function buildGraph(data) {
        nodes = [];
        edges = [];
        nodeMap = {};
        adjacency = {};

        var count = data.nodes.length;
        var angleStep = (2 * Math.PI) / count;
        var radius = Math.min(300, count * 12);

        data.nodes.forEach(function (n, i) {
            var angle = angleStep * i + (Math.random() - 0.5) * 0.5;
            var r = radius * (0.5 + Math.random() * 0.5);
            var initColor = TYPE_COLORS[n.type] || "#666";
            var rgb = hexToRgb(initColor);
            var node = {
                id: n.id,
                title: n.title,
                type: n.type,
                source_count: n.source_count || 0,
                tags: n.tags || [],
                summary: n.summary || "",
                created: n.created || "",
                updated: n.updated || "",
                x: Math.cos(angle) * r,
                y: Math.sin(angle) * r,
                vx: 0,
                vy: 0,
                radius: nodeRadius(n.source_count || 0),
                color: initColor
            };
            nodes.push(node);
            nodeMap[n.id] = node;
            adjacency[n.id] = [];
            nodeOpacities[n.id] = { current: 1, target: 1 };
            nodeColors[n.id] = {
                r: rgb.r, g: rgb.g, b: rgb.b,
                targetR: rgb.r, targetG: rgb.g, targetB: rgb.b
            };
        });

        data.edges.forEach(function (e, idx) {
            var fromNode = nodeMap[e.from];
            var toNode = nodeMap[e.to];
            if (!fromNode || !toNode) return;

            edges.push({
                from: e.from,
                to: e.to,
                type: e.type,
                tag: e.tag || null,
                idx: idx
            });

            adjacency[e.from].push({ edgeIdx: edges.length - 1, otherId: e.to });
            adjacency[e.to].push({ edgeIdx: edges.length - 1, otherId: e.from });
        });

        statsEl.textContent = data.nodes.length + " nodes \u00b7 " + data.edges.length + " edges";

        // Center camera on graph center of mass
        var cx = 0, cy = 0;
        nodes.forEach(function (n) { cx += n.x; cy += n.y; });
        if (nodes.length > 0) {
            camera.x = cx / nodes.length;
            camera.y = cy / nodes.length;
        }
    }

    function nodeRadius(sourceCount) {
        if (sourceCount <= 0) return 3;
        return Math.min(7, 3 + sourceCount * 0.4);
    }

    // ── Compute Preset Metadata ──

    function computePresetMetadata() {
        // Tag frequency map
        var tagFreq = {};
        nodes.forEach(function (n) {
            (n.tags || []).forEach(function (t) {
                tagFreq[t] = (tagFreq[t] || 0) + 1;
            });
        });

        // Sort by frequency, pick top 8
        var sorted = Object.keys(tagFreq).sort(function (a, b) {
            return tagFreq[b] - tagFreq[a];
        });
        topTags = sorted.slice(0, TAG_PALETTE.length);
        tagColorMap = {};
        topTags.forEach(function (tag, i) {
            tagColorMap[tag] = TAG_PALETTE[i];
        });

        // Date range
        var dates = [];
        nodes.forEach(function (n) {
            if (n.created) {
                var d = new Date(n.created);
                if (!isNaN(d.getTime())) dates.push(d);
            }
        });
        if (dates.length > 0) {
            dates.sort(function (a, b) { return a - b; });
            dateRange.min = dates[0];
            dateRange.max = dates[dates.length - 1];
        }

        // Degree range (number of edges per node)
        var minDeg = Infinity, maxDeg = 0;
        nodes.forEach(function (n) {
            var deg = (adjacency[n.id] || []).length;
            if (deg < minDeg) minDeg = deg;
            if (deg > maxDeg) maxDeg = deg;
        });
        degreeRange.min = minDeg === Infinity ? 0 : minDeg;
        degreeRange.max = maxDeg;

        // Source count range
        var minSrc = Infinity, maxSrc = 0;
        nodes.forEach(function (n) {
            var sc = n.source_count || 0;
            if (sc < minSrc) minSrc = sc;
            if (sc > maxSrc) maxSrc = sc;
        });
        sourceRange.min = minSrc === Infinity ? 0 : minSrc;
        sourceRange.max = maxSrc;
    }

    // ── Preset Color Functions ──

    function colorByType(node) {
        return TYPE_COLORS[node.type] || "#666";
    }

    function colorByTag(node) {
        var primaryTag = (node.tags && node.tags.length > 0) ? node.tags[0] : null;
        if (primaryTag && tagColorMap[primaryTag]) {
            return tagColorMap[primaryTag];
        }
        return TAG_DEFAULT_COLOR;
    }

    function colorByTimeline(node) {
        if (!node.created || !dateRange.min || !dateRange.max) return "#3399aa";
        var d = new Date(node.created);
        if (isNaN(d.getTime())) return "#3399aa";

        var span = dateRange.max.getTime() - dateRange.min.getTime();
        var t = span > 0 ? (d.getTime() - dateRange.min.getTime()) / span : 0.5;
        t = Math.max(0, Math.min(1, t));

        // Gradient: medium cyan (#2299aa) -> bright cyan (#00d2ff) -> near-white (#ccf5ff)
        var r, g, b;
        if (t < 0.5) {
            var t2 = t / 0.5;
            r = lerp(34, 0, t2);
            g = lerp(153, 210, t2);
            b = lerp(170, 255, t2);
        } else {
            var t2 = (t - 0.5) / 0.5;
            r = lerp(0, 204, t2);
            g = lerp(210, 245, t2);
            b = lerp(255, 255, t2);
        }
        return rgbToHex(Math.round(r), Math.round(g), Math.round(b));
    }

    function colorByConnections(node) {
        var deg = (adjacency[node.id] || []).length;
        var span = degreeRange.max - degreeRange.min;
        var t = span > 0 ? (deg - degreeRange.min) / span : 0;
        t = Math.max(0, Math.min(1, t));

        // Medium red (#aa3333) -> orange (#e07020) -> bright yellow (#ffdd44)
        var r, g, b;
        if (t < 0.5) {
            var t2 = t / 0.5;
            r = lerp(170, 224, t2);
            g = lerp(51, 112, t2);
            b = lerp(51, 32, t2);
        } else {
            var t2 = (t - 0.5) / 0.5;
            r = lerp(224, 255, t2);
            g = lerp(112, 221, t2);
            b = lerp(32, 68, t2);
        }
        return rgbToHex(Math.round(r), Math.round(g), Math.round(b));
    }

    function colorByDensity(node) {
        var sc = node.source_count || 0;
        var span = sourceRange.max - sourceRange.min;
        var t = span > 0 ? (sc - sourceRange.min) / span : 0;
        t = Math.max(0, Math.min(1, t));

        // Medium green (#228844) -> emerald (#33bb66) -> bright green (#6dffa0)
        var r, g, b;
        if (t < 0.5) {
            var t2 = t / 0.5;
            r = lerp(34, 51, t2);
            g = lerp(136, 187, t2);
            b = lerp(68, 102, t2);
        } else {
            var t2 = (t - 0.5) / 0.5;
            r = lerp(51, 109, t2);
            g = lerp(187, 255, t2);
            b = lerp(102, 160, t2);
        }
        return rgbToHex(Math.round(r), Math.round(g), Math.round(b));
    }

    var PRESET_FN = {
        "type": colorByType,
        "tag": colorByTag,
        "timeline": colorByTimeline,
        "connections": colorByConnections,
        "density": colorByDensity
    };

    // ── Apply Preset ──

    function applyPreset(presetName) {
        currentPreset = presetName;
        var fn = PRESET_FN[presetName] || colorByType;

        nodes.forEach(function (n) {
            var newHex = fn(n);
            var rgb = hexToRgb(newHex);
            var c = nodeColors[n.id];
            // Set both current and target immediately — no animation delay
            c.r = rgb.r;
            c.g = rgb.g;
            c.b = rgb.b;
            c.targetR = rgb.r;
            c.targetG = rgb.g;
            c.targetB = rgb.b;
            // Update node color immediately for rendering
            n.color = newHex;
        });

        // Update preset button label and dots
        presetLabel.textContent = presetDisplayName(presetName);
        updatePresetButtonDots(presetName);
        updatePresetDropdownActive(presetName);
        updateLegend();
    }

    function presetDisplayName(name) {
        var names = {
            "type": "Type",
            "tag": "Tag Cluster",
            "timeline": "Timeline",
            "connections": "Connections",
            "density": "Source Density"
        };
        return names[name] || name;
    }

    function updatePresetButtonDots(presetName) {
        var dotsContainer = presetBtn.querySelector(".preset-dots");
        var dots = dotsContainer.querySelectorAll(".dot");
        var colors;
        switch (presetName) {
            case "type":
                colors = ["#4a9eff", "#f59e0b", "#34d399"];
                break;
            case "tag":
                colors = ["#ff6b6b", "#4ecdc4", "#45b7d1"];
                break;
            case "timeline":
                colors = ["#2299aa", "#00d2ff", "#ccf5ff"];
                break;
            case "connections":
                colors = ["#aa3333", "#e07020", "#ffdd44"];
                break;
            case "density":
                colors = ["#228844", "#33bb66", "#6dffa0"];
                break;
            default:
                colors = ["#4a9eff", "#f59e0b", "#34d399"];
        }
        for (var i = 0; i < dots.length && i < colors.length; i++) {
            dots[i].style.background = colors[i];
        }
    }

    function updatePresetDropdownActive(presetName) {
        presetOptions.forEach(function (opt) {
            if (opt.getAttribute("data-preset") === presetName) {
                opt.classList.add("active");
            } else {
                opt.classList.remove("active");
            }
        });
    }

    // ── Legend ──

    function updateLegend() {
        var html = '';

        switch (currentPreset) {
            case "type":
                html += '<div class="legend-title">By Type</div>';
                html += '<div class="legend-items">';
                Object.keys(TYPE_COLORS).forEach(function (key) {
                    html += '<div class="legend-item">'
                        + '<span class="legend-dot" style="background:' + TYPE_COLORS[key] + '"></span>'
                        + '<span>' + TYPE_LABELS[key] + '</span></div>';
                });
                html += '</div>';
                break;

            case "tag":
                html += '<div class="legend-title">By Primary Tag</div>';
                html += '<div class="legend-items">';
                topTags.forEach(function (tag) {
                    html += '<div class="legend-item">'
                        + '<span class="legend-dot" style="background:' + tagColorMap[tag] + '"></span>'
                        + '<span>' + escapeHtml(tag) + '</span></div>';
                });
                html += '<div class="legend-item">'
                    + '<span class="legend-dot" style="background:#555"></span>'
                    + '<span>other</span></div>';
                html += '</div>';
                break;

            case "timeline":
                html += '<div class="legend-title">By Created Date</div>';
                html += '<div class="legend-gradient-row">';
                html += '<span class="legend-gradient-label">' + formatDate(dateRange.min) + '</span>';
                html += '<div class="legend-gradient-bar" style="background:linear-gradient(to right, #2299aa, #00d2ff, #ccf5ff)"></div>';
                html += '<span class="legend-gradient-label">' + formatDate(dateRange.max) + '</span>';
                html += '</div>';
                break;

            case "connections":
                html += '<div class="legend-title">By Connections</div>';
                html += '<div class="legend-gradient-row">';
                html += '<span class="legend-gradient-label">' + degreeRange.min + '</span>';
                html += '<div class="legend-gradient-bar" style="background:linear-gradient(to right, #aa3333, #e07020, #ffdd44)"></div>';
                html += '<span class="legend-gradient-label">' + degreeRange.max + '</span>';
                html += '</div>';
                break;

            case "density":
                html += '<div class="legend-title">By Source Count</div>';
                html += '<div class="legend-gradient-row">';
                html += '<span class="legend-gradient-label">' + sourceRange.min + '</span>';
                html += '<div class="legend-gradient-bar" style="background:linear-gradient(to right, #228844, #33bb66, #6dffa0)"></div>';
                html += '<span class="legend-gradient-label">' + sourceRange.max + '</span>';
                html += '</div>';
                break;
        }

        legendEl.innerHTML = html;

        // Show legend after a tick to trigger transition
        requestAnimationFrame(function () {
            legendEl.classList.add("visible");
        });
    }

    function formatDate(d) {
        if (!d) return "?";
        var m = d.getMonth() + 1;
        var day = d.getDate();
        return d.getFullYear() + "-" + (m < 10 ? "0" : "") + m + "-" + (day < 10 ? "0" : "") + day;
    }

    // ── Preset Dropdown Interactions ──

    presetBtn.addEventListener("click", function (e) {
        e.stopPropagation();
        presetDropdownOpen = !presetDropdownOpen;
        if (presetDropdownOpen) {
            presetDropdown.classList.remove("hidden");
        } else {
            presetDropdown.classList.add("hidden");
        }
    });

    presetOptions.forEach(function (opt) {
        opt.addEventListener("click", function (e) {
            e.stopPropagation();
            var preset = opt.getAttribute("data-preset");
            applyPreset(preset);
            presetDropdownOpen = false;
            presetDropdown.classList.add("hidden");
        });
    });

    // Close dropdown when clicking elsewhere
    document.addEventListener("click", function () {
        if (presetDropdownOpen) {
            presetDropdownOpen = false;
            presetDropdown.classList.add("hidden");
        }
    });

    // ── Physics: Force-Directed Layout ──

    function stepPhysics(dt) {
        if (physicsStopped) return;

        var dtClamped = Math.min(dt, 0.033); // cap at ~30fps equivalent
        var n = nodes.length;
        if (n === 0) return;

        // Reset forces
        var fx = new Float64Array(n);
        var fy = new Float64Array(n);

        // Repulsion (Coulomb's law) between all node pairs
        var REPULSION = 8000;
        for (var i = 0; i < n; i++) {
            var ni = nodes[i];
            if (nodeOpacities[ni.id].current < 0.05) continue;
            for (var j = i + 1; j < n; j++) {
                var nj = nodes[j];
                if (nodeOpacities[nj.id].current < 0.05) continue;
                var dx = ni.x - nj.x;
                var dy = ni.y - nj.y;
                var dist2 = dx * dx + dy * dy;
                if (dist2 < 1) dist2 = 1;
                var dist = Math.sqrt(dist2);
                var force = REPULSION / dist2;
                var forceX = (dx / dist) * force;
                var forceY = (dy / dist) * force;
                fx[i] += forceX;
                fy[i] += forceY;
                fx[j] -= forceX;
                fy[j] -= forceY;
            }
        }

        // Attraction along edges (Hooke's law)
        var SPRING = 0.008;
        var REST_LENGTH_WIKI = 120;
        var REST_LENGTH_TAG = 200;
        edges.forEach(function (e) {
            var a = nodeMap[e.from];
            var b = nodeMap[e.to];
            if (!a || !b) return;
            if (nodeOpacities[a.id].current < 0.05 || nodeOpacities[b.id].current < 0.05) return;

            var idxA = nodes.indexOf(a);
            var idxB = nodes.indexOf(b);
            var dx = b.x - a.x;
            var dy = b.y - a.y;
            var dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 0.1) dist = 0.1;

            var restLen = e.type === "wikilink" ? REST_LENGTH_WIKI : REST_LENGTH_TAG;
            var springK = e.type === "wikilink" ? SPRING : SPRING * 0.3;
            var displacement = dist - restLen;
            var force = springK * displacement;
            var forceX = (dx / dist) * force;
            var forceY = (dy / dist) * force;

            fx[idxA] += forceX;
            fy[idxA] += forceY;
            fx[idxB] -= forceX;
            fy[idxB] -= forceY;
        });

        // Central gravity
        var GRAVITY = 0.3;
        var cx = 0, cy = 0;
        nodes.forEach(function (nd) { cx += nd.x; cy += nd.y; });
        cx /= n;
        cy /= n;

        for (var k = 0; k < n; k++) {
            var nk = nodes[k];
            fx[k] += (cx - nk.x) * GRAVITY;
            fy[k] += (cy - nk.y) * GRAVITY;
        }

        // Apply forces with damping
        var DAMPING = 0.85;
        var MAX_VELOCITY = 80;
        var totalKinetic = 0;

        for (var m = 0; m < n; m++) {
            var nm = nodes[m];
            if (nm === dragNode) continue; // don't move dragged node
            if (nodeOpacities[nm.id].current < 0.05) continue;

            nm.vx = (nm.vx + fx[m] * dtClamped) * DAMPING;
            nm.vy = (nm.vy + fy[m] * dtClamped) * DAMPING;

            // Clamp velocity
            var speed = Math.sqrt(nm.vx * nm.vx + nm.vy * nm.vy);
            if (speed > MAX_VELOCITY) {
                nm.vx = (nm.vx / speed) * MAX_VELOCITY;
                nm.vy = (nm.vy / speed) * MAX_VELOCITY;
            }

            nm.x += nm.vx * dtClamped;
            nm.y += nm.vy * dtClamped;

            totalKinetic += nm.vx * nm.vx + nm.vy * nm.vy;
        }

        // Stabilization check
        if (totalKinetic < 0.5) {
            stabilizationCount++;
            if (stabilizationCount > STABILIZATION_THRESHOLD) {
                physicsStopped = true;
            }
        } else {
            stabilizationCount = 0;
        }
    }

    // ── Rendering ──

    function render(time) {
        var dt = lastTime ? (time - lastTime) / 1000 : 0.016;
        lastTime = time;

        // Animate breath and pulse
        breathPhase += dt * 0.5; // slow breathing
        pulsePhase += dt * 2.5;  // faster pulse for selected

        // Animate opacity fades
        nodes.forEach(function (n) {
            var op = nodeOpacities[n.id];
            if (Math.abs(op.current - op.target) > 0.01) {
                op.current += (op.target - op.current) * 0.08;
            } else {
                op.current = op.target;
            }
        });

        // Animate color transitions
        animateColors();

        // Physics step
        stepPhysics(dt);

        // Clear
        var rect = container.getBoundingClientRect();
        var w = rect.width;
        var h = rect.height;

        ctx.save();
        ctx.clearRect(0, 0, w, h);

        // Background with subtle radial gradient
        var bgGrad = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, Math.max(w, h) * 0.7);
        bgGrad.addColorStop(0, "#0f0f0f");
        bgGrad.addColorStop(1, "#0a0a0a");
        ctx.fillStyle = bgGrad;
        ctx.fillRect(0, 0, w, h);

        // Apply camera transform
        ctx.translate(w / 2, h / 2);
        ctx.scale(camera.zoom, camera.zoom);
        ctx.translate(-camera.x, -camera.y);

        // Draw edges
        drawEdges();

        // Draw nodes
        drawNodes();

        ctx.restore();

        animFrame = requestAnimationFrame(render);
    }

    function animateColors() {
        nodes.forEach(function (n) {
            var c = nodeColors[n.id];
            var dr = c.targetR - c.r;
            var dg = c.targetG - c.g;
            var db = c.targetB - c.b;

            if (Math.abs(dr) > 0.5 || Math.abs(dg) > 0.5 || Math.abs(db) > 0.5) {
                c.r += dr * COLOR_LERP_SPEED;
                c.g += dg * COLOR_LERP_SPEED;
                c.b += db * COLOR_LERP_SPEED;
            } else {
                c.r = c.targetR;
                c.g = c.targetG;
                c.b = c.targetB;
            }

            // Update the node's hex color for rendering
            n.color = rgbToHex(Math.round(c.r), Math.round(c.g), Math.round(c.b));
        });
    }

    function drawEdges() {
        var hovered = hoveredNodeId || selectedNodeId;
        var hoveredConns = {};
        if (hovered && adjacency[hovered]) {
            adjacency[hovered].forEach(function (c) {
                hoveredConns[c.edgeIdx] = true;
            });
        }

        edges.forEach(function (e, idx) {
            var fromNode = nodeMap[e.from];
            var toNode = nodeMap[e.to];
            if (!fromNode || !toNode) return;

            var fromOp = nodeOpacities[e.from].current;
            var toOp = nodeOpacities[e.to].current;
            var edgeOp = Math.min(fromOp, toOp);
            if (edgeOp < 0.02) return;

            var isWikilink = e.type === "wikilink";
            var isHighlighted = hoveredConns[idx];

            var baseAlpha, lineWidth, color;

            if (isHighlighted) {
                // Highlight: use the hovered node's color
                var hoveredNode = nodeMap[hovered];
                color = hoveredNode ? hoveredNode.color : "#4a9eff";
                baseAlpha = 0.6;
                lineWidth = isWikilink ? 1.2 : 0.7;
            } else {
                color = isWikilink ? "#444" : "#282828";
                baseAlpha = isWikilink ? 0.35 : 0.12;
                lineWidth = isWikilink ? 0.5 : 0.3;
            }

            ctx.beginPath();
            ctx.moveTo(fromNode.x, fromNode.y);
            ctx.lineTo(toNode.x, toNode.y);
            ctx.strokeStyle = color;
            ctx.globalAlpha = baseAlpha * edgeOp;
            ctx.lineWidth = lineWidth / camera.zoom; // keep visual thickness consistent
            ctx.stroke();
            ctx.globalAlpha = 1;
        });
    }

    function drawNodes() {
        var breathOffset = Math.sin(breathPhase * Math.PI * 2 / 3.5) * 1.0; // +-1px over ~3.5s
        var pulseOffset = Math.sin(pulsePhase * Math.PI * 2 / 1.5) * 0.4;  // subtle pulse

        var hovered = hoveredNodeId;
        var selected = selectedNodeId;
        var connectedToHover = {};
        if (hovered && adjacency[hovered]) {
            adjacency[hovered].forEach(function (c) {
                connectedToHover[c.otherId] = true;
            });
        }

        // Draw in two passes: non-hovered first, then hovered/selected on top
        var sortedNodes = nodes.slice().sort(function (a, b) {
            var aTop = (a.id === hovered || a.id === selected) ? 1 : 0;
            var bTop = (b.id === hovered || b.id === selected) ? 1 : 0;
            return aTop - bTop;
        });

        sortedNodes.forEach(function (n) {
            var opacity = nodeOpacities[n.id].current;
            if (opacity < 0.02) return;

            var isHovered = n.id === hovered;
            var isSelected = n.id === selected;
            var isConnected = connectedToHover[n.id];

            var coreRadius = n.radius;
            var glowRadius = coreRadius * 2.8;
            var glowAlpha = 0.25;
            var coreAlpha = 0.85;

            // Breathing animation
            glowRadius += breathOffset;

            if (isSelected) {
                glowAlpha = 0.5 + pulseOffset * 0.2;
                coreAlpha = 1.0;
                glowRadius = coreRadius * 3.5 + Math.abs(pulseOffset) * 2;
            }

            if (isHovered) {
                glowAlpha = 0.6;
                coreAlpha = 1.0;
                glowRadius = coreRadius * 3.5;
            }

            if (isConnected && !isHovered && !isSelected) {
                glowAlpha = 0.4;
                coreAlpha = 0.95;
                glowRadius = coreRadius * 3.0;
            }

            var rgb = hexToRgb(n.color);

            // Draw outer glow (using shadowBlur for smooth gaussian effect)
            ctx.save();
            ctx.globalAlpha = glowAlpha * opacity;
            ctx.shadowBlur = glowRadius * 2;
            ctx.shadowColor = n.color;
            ctx.beginPath();
            ctx.arc(n.x, n.y, coreRadius * 0.5, 0, Math.PI * 2);
            ctx.fillStyle = n.color;
            ctx.fill();
            ctx.restore();

            // Draw second glow layer for extra bloom
            ctx.save();
            ctx.globalAlpha = glowAlpha * 0.3 * opacity;
            ctx.shadowBlur = glowRadius * 4;
            ctx.shadowColor = n.color;
            ctx.beginPath();
            ctx.arc(n.x, n.y, coreRadius * 0.3, 0, Math.PI * 2);
            ctx.fillStyle = n.color;
            ctx.fill();
            ctx.restore();

            // Draw radial gradient glow (manual, for precision)
            var grad = ctx.createRadialGradient(n.x, n.y, coreRadius * 0.3, n.x, n.y, glowRadius);
            grad.addColorStop(0, "rgba(" + rgb.r + "," + rgb.g + "," + rgb.b + "," + (0.4 * opacity) + ")");
            grad.addColorStop(0.4, "rgba(" + rgb.r + "," + rgb.g + "," + rgb.b + "," + (0.15 * opacity) + ")");
            grad.addColorStop(1, "rgba(" + rgb.r + "," + rgb.g + "," + rgb.b + ",0)");
            ctx.beginPath();
            ctx.arc(n.x, n.y, glowRadius, 0, Math.PI * 2);
            ctx.fillStyle = grad;
            ctx.fill();

            // Draw solid core
            ctx.save();
            ctx.globalAlpha = coreAlpha * opacity;
            ctx.beginPath();
            ctx.arc(n.x, n.y, coreRadius, 0, Math.PI * 2);
            // Core gradient: lighter center, colored edge
            var coreGrad = ctx.createRadialGradient(
                n.x - coreRadius * 0.3, n.y - coreRadius * 0.3, 0,
                n.x, n.y, coreRadius
            );
            coreGrad.addColorStop(0, lighten(n.color, 0.5));
            coreGrad.addColorStop(1, n.color);
            ctx.fillStyle = coreGrad;
            ctx.fill();
            ctx.restore();

            // Draw label
            var showLabel = isHovered || isSelected || isConnected || n.source_count > 5;
            if (showLabel && opacity > 0.3) {
                var fontSize = Math.max(10, Math.min(13, 9 + n.source_count * 0.3));
                var labelAlpha = isHovered || isSelected ? 1.0 : isConnected ? 0.8 : 0.6;

                ctx.save();
                ctx.globalAlpha = labelAlpha * opacity;
                ctx.font = fontSize + "px -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif";
                ctx.textAlign = "center";
                ctx.textBaseline = "top";

                // Text shadow for readability
                ctx.shadowBlur = 6;
                ctx.shadowColor = "rgba(0,0,0,0.9)";
                ctx.shadowOffsetX = 0;
                ctx.shadowOffsetY = 0;
                ctx.fillStyle = "#e0e0e0";
                ctx.fillText(n.title, n.x, n.y + coreRadius + 6);

                ctx.restore();
            }
        });
    }

    // ── Animation Loop ──

    function startAnimation() {
        animFrame = requestAnimationFrame(render);
    }

    // ── Hit Testing ──

    function worldFromScreen(sx, sy) {
        var rect = container.getBoundingClientRect();
        var w = rect.width;
        var h = rect.height;
        return {
            x: (sx - w / 2) / camera.zoom + camera.x,
            y: (sy - h / 2) / camera.zoom + camera.y
        };
    }

    function screenFromWorld(wx, wy) {
        var rect = container.getBoundingClientRect();
        var w = rect.width;
        var h = rect.height;
        return {
            x: (wx - camera.x) * camera.zoom + w / 2,
            y: (wy - camera.y) * camera.zoom + h / 2
        };
    }

    function hitTest(sx, sy) {
        var world = worldFromScreen(sx, sy);
        var hitRadius = 12 / camera.zoom; // generous click area
        var closest = null;
        var closestDist = Infinity;

        nodes.forEach(function (n) {
            if (nodeOpacities[n.id].current < 0.1) return;
            var dx = world.x - n.x;
            var dy = world.y - n.y;
            var dist = Math.sqrt(dx * dx + dy * dy);
            var threshold = Math.max(n.radius, hitRadius);
            if (dist < threshold && dist < closestDist) {
                closest = n;
                closestDist = dist;
            }
        });

        return closest;
    }

    // ── Interaction: Mouse Events ──

    canvas.addEventListener("mousedown", function (e) {
        var rect = canvas.getBoundingClientRect();
        var mx = e.clientX - rect.left;
        var my = e.clientY - rect.top;

        var hit = hitTest(mx, my);
        if (hit) {
            dragNode = hit;
            dragNode.vx = 0;
            dragNode.vy = 0;
        } else {
            isPanning = true;
            panStart = { x: e.clientX, y: e.clientY };
            panCameraStart = { x: camera.x, y: camera.y };
        }
    });

    canvas.addEventListener("mousemove", function (e) {
        var rect = canvas.getBoundingClientRect();
        var mx = e.clientX - rect.left;
        var my = e.clientY - rect.top;

        if (dragNode) {
            var world = worldFromScreen(mx, my);
            dragNode.x = world.x;
            dragNode.y = world.y;
            dragNode.vx = 0;
            dragNode.vy = 0;
            canvas.style.cursor = "grabbing";
            return;
        }

        if (isPanning) {
            var dx = (e.clientX - panStart.x) / camera.zoom;
            var dy = (e.clientY - panStart.y) / camera.zoom;
            camera.x = panCameraStart.x - dx;
            camera.y = panCameraStart.y - dy;
            canvas.style.cursor = "grabbing";
            return;
        }

        // Hover detection
        var hit = hitTest(mx, my);
        var newHovered = hit ? hit.id : null;
        if (newHovered !== hoveredNodeId) {
            hoveredNodeId = newHovered;
            canvas.style.cursor = newHovered ? "pointer" : "default";
        }
    });

    canvas.addEventListener("mouseup", function (e) {
        if (dragNode) {
            // If it was just a click (no significant drag), treat as selection
            dragNode = null;
        }
        isPanning = false;
        canvas.style.cursor = hoveredNodeId ? "pointer" : "default";
    });

    canvas.addEventListener("click", function (e) {
        var rect = canvas.getBoundingClientRect();
        var mx = e.clientX - rect.left;
        var my = e.clientY - rect.top;

        var hit = hitTest(mx, my);
        if (hit) {
            selectedNodeId = hit.id;
            showDetail(hit.id);
            // Re-enable physics briefly for settle
        } else {
            selectedNodeId = null;
            hideDetail();
        }
    });

    // Zoom with scroll wheel
    canvas.addEventListener("wheel", function (e) {
        e.preventDefault();
        var rect = canvas.getBoundingClientRect();
        var mx = e.clientX - rect.left;
        var my = e.clientY - rect.top;

        // World position under cursor before zoom
        var worldBefore = worldFromScreen(mx, my);

        var zoomFactor = e.deltaY > 0 ? 0.92 : 1.08;
        camera.zoom = Math.max(0.15, Math.min(5, camera.zoom * zoomFactor));

        // World position under cursor after zoom
        var worldAfter = worldFromScreen(mx, my);

        // Adjust camera so cursor stays on same world point
        camera.x += worldBefore.x - worldAfter.x;
        camera.y += worldBefore.y - worldAfter.y;
    }, { passive: false });

    // Touch support for mobile
    var lastTouchDist = 0;
    var lastTouchCenter = { x: 0, y: 0 };

    canvas.addEventListener("touchstart", function (e) {
        if (e.touches.length === 1) {
            var touch = e.touches[0];
            var rect = canvas.getBoundingClientRect();
            var mx = touch.clientX - rect.left;
            var my = touch.clientY - rect.top;
            var hit = hitTest(mx, my);
            if (hit) {
                dragNode = hit;
            } else {
                isPanning = true;
                panStart = { x: touch.clientX, y: touch.clientY };
                panCameraStart = { x: camera.x, y: camera.y };
            }
        } else if (e.touches.length === 2) {
            var t1 = e.touches[0];
            var t2 = e.touches[1];
            lastTouchDist = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
            lastTouchCenter = {
                x: (t1.clientX + t2.clientX) / 2,
                y: (t1.clientY + t2.clientY) / 2
            };
        }
        e.preventDefault();
    }, { passive: false });

    canvas.addEventListener("touchmove", function (e) {
        if (e.touches.length === 1) {
            var touch = e.touches[0];
            var rect = canvas.getBoundingClientRect();
            var mx = touch.clientX - rect.left;
            var my = touch.clientY - rect.top;

            if (dragNode) {
                var world = worldFromScreen(mx, my);
                dragNode.x = world.x;
                dragNode.y = world.y;
            } else if (isPanning) {
                var dx = (touch.clientX - panStart.x) / camera.zoom;
                var dy = (touch.clientY - panStart.y) / camera.zoom;
                camera.x = panCameraStart.x - dx;
                camera.y = panCameraStart.y - dy;
            }
        } else if (e.touches.length === 2) {
            var t1 = e.touches[0];
            var t2 = e.touches[1];
            var dist = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
            var scale = dist / lastTouchDist;
            camera.zoom = Math.max(0.15, Math.min(5, camera.zoom * scale));
            lastTouchDist = dist;
        }
        e.preventDefault();
    }, { passive: false });

    canvas.addEventListener("touchend", function () {
        dragNode = null;
        isPanning = false;
    });

    // ── Detail Panel ──

    function showDetail(nodeId) {
        var n = nodeMap[nodeId];
        if (!n) return;

        selectedNodeId = nodeId;

        var conns = adjacency[nodeId] || [];
        var wikilinks = [];
        var tagLinks = [];
        var seenTags = {};

        conns.forEach(function (c) {
            var edge = edges[c.edgeIdx];
            var other = nodeMap[c.otherId];
            if (!edge || !other) return;

            var entry = { id: c.otherId, title: other.title };
            if (edge.type === "wikilink") {
                wikilinks.push(entry);
            } else {
                if (!seenTags[c.otherId]) {
                    entry.tag = edge.tag;
                    tagLinks.push(entry);
                    seenTags[c.otherId] = true;
                }
            }
        });

        // De-duplicate wikilinks
        var seenWiki = {};
        wikilinks = wikilinks.filter(function (w) {
            if (seenWiki[w.id]) return false;
            seenWiki[w.id] = true;
            return true;
        });

        var typeClass = n.type;
        var typeLabel = TYPE_LABELS[n.type] || n.type;

        var html = '<button class="panel-close" onclick="window._closePanel()">\u00d7</button>';
        html += '<div class="panel-title">' + escapeHtml(n.title) + '</div>';
        html += '<span class="type-badge ' + typeClass + '">' + typeLabel + '</span>';

        if (n.summary) {
            html += '<div class="panel-summary">' + escapeHtml(n.summary) + '</div>';
        }

        if (n.tags && n.tags.length > 0) {
            html += '<div class="panel-tags">';
            n.tags.forEach(function (tag) {
                html += '<span class="panel-tag">' + escapeHtml(tag) + '</span>';
            });
            html += '</div>';
        }

        if (wikilinks.length > 0) {
            html += '<div class="panel-section">';
            html += '<div class="panel-section-title">Direct Links (' + wikilinks.length + ')</div>';
            html += '<ul class="connection-list">';
            wikilinks.forEach(function (link) {
                html += '<li onclick="window._focusNode(\'' + escapeAttr(link.id) + '\')">'
                    + escapeHtml(link.title) + '</li>';
            });
            html += '</ul></div>';
        }

        if (tagLinks.length > 0) {
            html += '<div class="panel-section">';
            html += '<div class="panel-section-title">Related by Tag (' + tagLinks.length + ')</div>';
            html += '<ul class="connection-list">';
            tagLinks.forEach(function (link) {
                var suffix = link.tag ? ' <span style="color:#555;font-size:0.6875rem">' + escapeHtml(link.tag) + '</span>' : '';
                html += '<li onclick="window._focusNode(\'' + escapeAttr(link.id) + '\')">'
                    + escapeHtml(link.title) + suffix + '</li>';
            });
            html += '</ul></div>';
        }

        html += '<div class="panel-meta">';
        if (n.created) html += 'Created: <span>' + escapeHtml(n.created) + '</span><br>';
        if (n.updated) html += 'Updated: <span>' + escapeHtml(n.updated) + '</span><br>';
        html += 'Sources: <span>' + n.source_count + '</span>';
        html += '</div>';

        detailPanel.innerHTML = html;
        detailPanel.classList.remove("hidden");
        detailPanel.classList.add("visible");
        container.classList.add("with-panel");

        // Resize canvas after panel animation
        setTimeout(resizeCanvas, 280);
    }

    function hideDetail() {
        selectedNodeId = null;
        detailPanel.classList.remove("visible");
        detailPanel.classList.add("hidden");
        container.classList.remove("with-panel");
        setTimeout(resizeCanvas, 280);
    }

    // ── Global handlers ──

    window._closePanel = function () {
        hideDetail();
    };

    window._focusNode = function (nodeId) {
        var n = nodeMap[nodeId];
        if (!n) return;

        // Smooth animate camera to node
        animateCamera(n.x, n.y, 1.5, 600);
        setTimeout(function () {
            showDetail(nodeId);
        }, 200);
    };

    function animateCamera(targetX, targetY, targetZoom, duration) {
        var startX = camera.x;
        var startY = camera.y;
        var startZoom = camera.zoom;
        var startTime = performance.now();

        function step(time) {
            var elapsed = time - startTime;
            var t = Math.min(1, elapsed / duration);
            // ease-in-out
            t = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;

            camera.x = startX + (targetX - startX) * t;
            camera.y = startY + (targetY - startY) * t;
            camera.zoom = startZoom + (targetZoom - startZoom) * t;

            if (t < 1) {
                requestAnimationFrame(step);
            }
        }
        requestAnimationFrame(step);
    }

    // ── Search ──

    searchBox.addEventListener("input", function () {
        var query = searchBox.value.trim().toLowerCase();
        if (!query || nodes.length === 0) return;

        var match = null;
        nodes.forEach(function (n) {
            if (match) return;
            var title = (n.title || "").toLowerCase();
            var summary = (n.summary || "").toLowerCase();
            if (title.indexOf(query) !== -1 || summary.indexOf(query) !== -1) {
                match = n;
            }
        });

        if (match) {
            window._focusNode(match.id);
        }
    });

    // ── Filter Buttons ──

    filterButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
            var type = btn.getAttribute("data-type");
            btn.classList.toggle("active");

            if (btn.classList.contains("active")) {
                hiddenTypes[type] = true;
            } else {
                delete hiddenTypes[type];
            }

            applyFilters();
        });
    });

    function applyFilters() {
        var activeFilters = Object.keys(hiddenTypes);
        var hasFilter = activeFilters.length > 0;

        nodes.forEach(function (n) {
            if (hasFilter) {
                var visible = activeFilters.indexOf(n.type) !== -1;
                nodeOpacities[n.id].target = visible ? 1 : 0;
            } else {
                nodeOpacities[n.id].target = 1;
            }
        });

        // Wake physics to re-settle
        if (physicsStopped) {
            physicsStopped = false;
            stabilizationCount = 0;
        }
    }

    // ── Loading ──

    function hideLoading() {
        loadingOverlay.classList.add("fade-out");
        setTimeout(function () {
            loadingOverlay.style.display = "none";
        }, 400);
    }

    // ── Utilities ──

    function hexToRgb(hex) {
        var r = parseInt(hex.slice(1, 3), 16);
        var g = parseInt(hex.slice(3, 5), 16);
        var b = parseInt(hex.slice(5, 7), 16);
        return { r: r, g: g, b: b };
    }

    function rgbToHex(r, g, b) {
        return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
    }

    function lighten(hex, amount) {
        var rgb = hexToRgb(hex);
        var r = Math.min(255, Math.round(rgb.r + (255 - rgb.r) * amount));
        var g = Math.min(255, Math.round(rgb.g + (255 - rgb.g) * amount));
        var b = Math.min(255, Math.round(rgb.b + (255 - rgb.b) * amount));
        return "rgb(" + r + "," + g + "," + b + ")";
    }

    function lerp(a, b, t) {
        return a + (b - a) * t;
    }

    function escapeHtml(str) {
        if (!str) return "";
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }

    function escapeAttr(str) {
        if (!str) return "";
        return str.replace(/'/g, "\\'").replace(/"/g, "&quot;");
    }

})();
