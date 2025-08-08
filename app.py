<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Intraday Astro–Gann Swing Tool</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-dark: #0a0e27;
            --primary-blue: #1a237e;
            --secondary-blue: #283593;
            --accent-purple: #3f51b5;
            --light-blue: #e8eaf6;
            --card-bg: #c5cae9;
            --gold: #ffd700;
            --silver: #c0c0c0;
            --gradient-cosmic: linear-gradient(135deg, #0a0e27 0%, #1a237e 50%, #283593 100%);
            --gradient-card: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
            --shadow-primary: 0 8px 32px rgba(26, 35, 126, 0.2);
            --shadow-card: 0 4px 20px rgba(0, 0, 0, 0.1);
            --text-primary: #0a0e27;
            --text-secondary: #64748b;
            --border-radius: 16px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--gradient-cosmic);
            min-height: 100vh;
            color: var(--text-primary);
            line-height: 1.6;
        }

        .cosmic-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 50%, rgba(255, 215, 0, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(63, 81, 181, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 80%, rgba(26, 35, 126, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            position: relative;
            z-index: 1;
        }

        .header {
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.95);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-primary);
            backdrop-filter: blur(10px);
        }

        .header h1 {
            font-size: 3.5rem;
            background: var(--gradient-cosmic);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        .header .subtitle {
            font-size: 1.2rem;
            color: var(--text-secondary);
            font-weight: 400;
        }

        .planet-icons {
            margin-top: 1.5rem;
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .planet-icon {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            transition: var(--transition);
            cursor: pointer;
        }

        .planet-icon:hover {
            transform: translateY(-2px) scale(1.1);
        }

        .planet-sun { background: linear-gradient(45deg, #ff6b35, #ffd700); }
        .planet-moon { background: linear-gradient(45deg, #c0c0c0, #f8f8ff); }
        .planet-mercury { background: linear-gradient(45deg, #87ceeb, #4682b4); }
        .planet-venus { background: linear-gradient(45deg, #ff69b4, #ffc0cb); }
        .planet-mars { background: linear-gradient(45deg, #dc143c, #ff4500); }
        .planet-jupiter { background: linear-gradient(45deg, #daa520, #ff8c00); }
        .planet-saturn { background: linear-gradient(45deg, #2f4f4f, #708090); }

        .controls-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }

        .control-card {
            background: var(--gradient-card);
            border-radius: var(--border-radius);
            padding: 2rem;
            box-shadow: var(--shadow-card);
            border: 1px solid rgba(63, 81, 181, 0.1);
            transition: var(--transition);
        }

        .control-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(26, 35, 126, 0.15);
        }

        .control-card h3 {
            color: var(--primary-blue);
            margin-bottom: 1.5rem;
            font-size: 1.25rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
            font-weight: 500;
            font-size: 0.95rem;
        }

        .form-input {
            width: 100%;
            padding: 0.875rem 1rem;
            border: 2px solid rgba(63, 81, 181, 0.2);
            border-radius: 12px;
            font-size: 1rem;
            transition: var(--transition);
            background: rgba(255, 255, 255, 0.8);
        }

        .form-input:focus {
            outline: none;
            border-color: var(--accent-purple);
            box-shadow: 0 0 0 3px rgba(63, 81, 181, 0.1);
        }

        .radio-group {
            display: flex;
            gap: 1rem;
            margin-top: 0.5rem;
        }

        .radio-option {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 8px;
            transition: var(--transition);
        }

        .radio-option:hover {
            background: rgba(63, 81, 181, 0.05);
        }

        .generate-btn {
            background: var(--gradient-cosmic);
            color: white;
            border: none;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            width: 100%;
            margin-top: 1rem;
            position: relative;
            overflow: hidden;
        }

        .generate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(26, 35, 126, 0.3);
        }

        .generate-btn:active {
            transform: translateY(0);
        }

        .market-status {
            background: rgba(255, 255, 255, 0.95);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin-bottom: 2rem;
            border-left: 5px solid var(--gold);
            box-shadow: var(--shadow-card);
        }

        .market-status h3 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .important-planet {
            background: linear-gradient(135deg, #ffd700, #ffecb3);
            border-radius: var(--border-radius);
            padding: 2rem;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: var(--shadow-card);
            border: 2px solid var(--gold);
        }

        .important-planet h2 {
            color: var(--primary-dark);
            margin-bottom: 1rem;
            font-size: 1.8rem;
        }

        .results-section {
            background: rgba(255, 255, 255, 0.95);
            border-radius: var(--border-radius);
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-primary);
        }

        .results-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .results-title {
            color: var(--primary-blue);
            font-size: 1.8rem;
            font-weight: 600;
        }

        .symbol-display {
            background: var(--gradient-cosmic);
            color: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            font-size: 1.2rem;
        }

        .transit-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .transit-card {
            background: var(--gradient-card);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid rgba(63, 81, 181, 0.1);
            transition: var(--transition);
        }

        .transit-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-card);
        }

        .transit-card h4 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .data-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: var(--shadow-card);
            background: white;
        }

        .data-table th,
        .data-table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
        }

        .data-table th {
            background: var(--gradient-cosmic);
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.875rem;
            letter-spacing: 0.5px;
        }

        .data-table tr:hover {
            background: rgba(63, 81, 181, 0.02);
        }

        .favorable-row {
            background: rgba(76, 175, 80, 0.1) !important;
            border-left: 4px solid #4caf50;
        }

        .negative-row {
            background: rgba(244, 67, 54, 0.1) !important;
            border-left: 4px solid #f44336;
        }

        .important-row {
            background: rgba(255, 215, 0, 0.2) !important;
            font-weight: 600;
            border-left: 4px solid var(--gold);
        }

        .current-transit-row {
            background: rgba(255, 152, 0, 0.2) !important;
            border: 2px solid #ff9800;
            position: relative;
        }

        .current-transit-row::after {
            content: "⚡";
            position: absolute;
            top: 50%;
            right: 1rem;
            transform: translateY(-50%);
            font-size: 1.2rem;
            color: #ff9800;
        }

        .download-section {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
            flex-wrap: wrap;
        }

        .download-btn {
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid var(--accent-purple);
            color: var(--accent-purple);
            padding: 0.875rem 1.5rem;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .download-btn:hover {
            background: var(--accent-purple);
            color: white;
            transform: translateY(-2px);
        }

        .footer {
            text-align: center;
            margin-top: 3rem;
            padding: 2rem;
            color: rgba(255, 255, 255, 0.8);
        }

        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .header h1 {
                font-size: 2.5rem;
            }
            
            .controls-grid {
                grid-template-columns: 1fr;
            }
            
            .results-header {
                flex-direction: column;
                text-align: center;
            }
            
            .data-table {
                font-size: 0.875rem;
            }
            
            .data-table th,
            .data-table td {
                padding: 0.75rem 0.5rem;
            }
        }

        .loading {
            display: none;
            text-align: center;
            padding: 2rem;
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(63, 81, 181, 0.1);
            border-top: 4px solid var(--accent-purple);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .alert {
            padding: 1rem 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .alert-warning {
            background: #fff3cd;
            border: 1px solid #ffc107;
            color: #664d03;
        }

        .alert-error {
            background: #f8d7da;
            border: 1px solid #dc3545;
            color: #721c24;
        }

        .alert-success {
            background: #d1e7dd;
            border: 1px solid #198754;
            color: #0f5132;
        }
    </style>
</head>
<body>
    <div class="cosmic-background"></div>
    
    <div class="container">
        <header class="header">
            <h1>Intraday Astro–Gann Swing Tool</h1>
            <p class="subtitle">Advanced Planetary Transit Analysis for Intraday Trading</p>
            <div class="planet-icons">
                <div class="planet-icon planet-sun" title="Sun">☉</div>
                <div class="planet-icon planet-moon" title="Moon">☽</div>
                <div class="planet-icon planet-mercury" title="Mercury">☿</div>
                <div class="planet-icon planet-venus" title="Venus">♀</div>
                <div class="planet-icon planet-mars" title="Mars">♂</div>
                <div class="planet-icon planet-jupiter" title="Jupiter">♃</div>
                <div class="planet-icon planet-saturn" title="Saturn">♄</div>
            </div>
        </header>

        <div class="controls-grid">
            <div class="control-card">
                <h3><i class="fas fa-calendar-alt"></i> Date & Time Settings</h3>
                <div class="form-group">
                    <label for="date">Select Date</label>
                    <input type="date" id="date" class="form-input" value="2024-08-08">
                </div>
                <div class="form-group">
                    <label for="time">Select Time</label>
                    <input type="time" id="time" class="form-input" value="09:15">
                </div>
                <div class="form-group">
                    <label for="location">Location</label>
                    <input type="text" id="location" class="form-input" value="Mumbai, India" placeholder="Enter location">
                </div>
            </div>

            <div class="control-card">
                <h3><i class="fas fa-chart-line"></i> Market Settings</h3>
                <div class="form-group">
                    <label for="symbol">Symbol</label>
                    <input type="text" id="symbol" class="form-input" value="Nifty" placeholder="Enter symbol">
                </div>
                <div class="form-group">
                    <label for="cmp">CMP (Current Market Price)</label>
                    <input type="number" id="cmp" class="form-input" value="24574.00" step="0.01">
                </div>
                <div class="form-group">
                    <label>Market Type</label>
                    <div class="radio-group">
                        <label class="radio-option">
                            <input type="radio" name="market" value="indian" checked>
                            <span>Indian Market</span>
                        </label>
                        <label class="radio-option">
                            <input type="radio" name="market" value="global">
                            <span>Global Market</span>
                        </label>
                    </div>
                </div>
            </div>

            <div class="control-card">
                <h3><i class="fas fa-cogs"></i> Advanced Settings</h3>
                <div class="form-group">
                    <label for="font-size">Table Font Size: <span id="font-size-value">16px</span></label>
                    <input type="range" id="font-size" class="form-input" min="12" max="24" value="16">
                </div>
                <div class="form-group">
                    <label for="swing-multiplier">Swing Range Multiplier: <span id="swing-value">1.0x</span></label>
                    <input type="range" id="swing-multiplier" class="form-input" min="0.5" max="3.0" value="1.0" step="0.1">
                </div>
                <div class="form-group">
                    <label for="bg-color">Background Color</label>
                    <input type="color" id="bg-color" class="form-input" value="#e8eaf6">
                </div>
            </div>
        </div>

        <button class="generate-btn" onclick="generateReport()">
            <i class="fas fa-magic"></i> Generate Astro-Gann Report
        </button>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Calculating planetary positions and market analysis...</p>
        </div>

        <div class="market-status">
            <h3><i class="fas fa-clock"></i> Market Status</h3>
            <p><strong>Indian Market Hours:</strong> 09:15 AM – 03:15 PM IST</p>
            <p><strong>Global Market Hours:</strong> 05:00 AM – 11:35 PM UTC</p>
            <p><strong>Current Status:</strong> <span class="status-indicator">Market Open</span></p>
        </div>

        <div class="important-planet">
            <h2><i class="fas fa-star"></i> Important Planet for Trading: Jupiter</h2>
            <p>The ruling planet for Friday is Venus. Pay special attention to its transit and levels during the trading session.</p>
        </div>

        <div class="results-section">
            <div class="results-header">
                <h2 class="results-title"><i class="fas fa-chart-area"></i> Planetary Transit Analysis</h2>
                <div class="symbol-display">Nifty | CMP: ₹24,574.00</div>
            </div>

            <div class="transit-grid">
                <div class="transit-card">
                    <h4><i class="fas fa-moon"></i> Moon-Rahu Transit</h4>
                    <p>Moon-Rahu 60°: 11:30 AM</p>
                    <p>Moon-Rahu 90°: 02:15 PM</p>
                    <p>Moon-Rahu 120°: 04:45 PM</p>
                </div>
                <div class="transit-card">
                    <h4><i class="fas fa-moon"></i> Moon-Ketu Transit</h4>
                    <p>Moon-Ketu 60°: 10:45 AM</p>
                    <p>Moon-Ketu 180°: 01:30 PM</p>
                    <p>Moon-Ketu 120°: 03:20 PM</p>
                </div>
            </div>

            <h3 style="color: var(--primary-blue); margin-bottom: 1.5rem;">
                <i class="fas fa-table"></i> Intraday Swing Range
            </h3>

            <div style="overflow-x: auto;">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Symbol</th>
                            <th>CMP</th>
                            <th>Swing Low</th>
                            <th>Swing High</th>
                            <th>Degree Range</th>
                            <th>Key Planet</th>
                            <th>Timing (IST)</th>
                            <th>Transit Nature</th>
                            <th>Important</th>
                            <th>Current Transit</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="current-transit-row important-row">
                            <td>Nifty</td>
                            <td>₹24,574.00</td>
                            <td>₹24,450.20</td>
                            <td>₹24,697.80</td>
                            <td>118.2°–124.8°</td>
                            <td>Venus in Swati</td>
                            <td>09:15 AM – 10:45 AM</td>
                            <td>Favorable</td>
                            <td>Yes</td>
                            <td>Yes</td>
                        </tr>
                        <tr class="favorable-row">
                            <td>Nifty</td>
                            <td>₹24,574.00</td>
                            <td>₹24,500.15</td>
                            <td>₹24,647.85</td>
                            <td>215.5°–221.1°</td>
                            <td>Jupiter</td>
                            <td>11:20 AM – 01:20 PM</td>
                            <td>Favorable</td>
                            <td>No</td>
                            <td>No</td>
                        </tr>
                        <tr class="negative-row">
                            <td>Nifty</td>
                            <td>₹24,574.00</td>
                            <td>₹24,525.30</td>
                            <td>₹24,622.70</td>
                            <td>95.8°–98.2°</td>
                            <td>Mars</td>
                            <td>02:30 PM – 03:15 PM</td>
                            <td>Negative</td>
                            <td>No</td>
                            <td>No</td>
                        </tr>
                        <tr>
                            <td>Nifty</td>
                            <td>₹24,574.00</td>
                            <td>₹24,535.40</td>
                            <td>₹24,612.60</td>
                            <td>183.7°–186.3°</td>
                            <td>Moon in Chitra</td>
                            <td>12:45 PM – 02:15 PM</td>
                            <td>Neutral</td>
                            <td>No</td>
                            <td>No</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="download-section">
                <button class="download-btn">
                    <i class="fas fa-file-pdf"></i> Download PDF
                </button>
                <button class="download-btn">
                    <i class="fas fa-file-excel"></i> Download Excel
                </button>
                <button class="download-btn">
                    <i class="fas fa-share-alt"></i> Share Report
                </button>
            </div>
        </div>

        <footer class="footer">
            <p>&copy; 2024 Astro-Gann Trading Tool. Combining ancient wisdom with modern market analysis.</p>
            <p><i class="fas fa-star"></i> May the stars guide your trades <i class="fas fa-star"></i></p>
        </footer>
    </div>

    <script>
        // Font size slider
        document.getElementById('font-size').addEventListener('input', function() {
            const value = this.value;
            document.getElementById('font-size-value').textContent = value + 'px';
            document.querySelector('.data-table').style.fontSize = value + 'px';
        });

        // Swing multiplier slider
        document.getElementById('swing-multiplier').addEventListener('input', function() {
            const value = this.value;
            document.getElementById('swing-value').textContent = value + 'x';
        });

        // Generate report function
        function generateReport() {
            const loading = document.getElementById('loading');
            const generateBtn = document.querySelector('.generate-btn');
            
            // Show loading animation
            loading.style.display = 'block';
            generateBtn.disabled = true;
            generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Calculating...';
            
            // Simulate API call
            setTimeout(() => {
                loading.style.display = 'none';
                generateBtn.disabled = false;
                generateBtn.innerHTML = '<i class="fas fa-magic"></i> Generate Astro-Gann Report';
                
                // Show success message
                const alert = document.createElement('div');
                alert.className = 'alert alert-success';
                alert.innerHTML = '<i class="fas fa-check-circle"></i> Report generated successfully!';
                document.querySelector('.results-section').insertBefore(alert, document.querySelector('.results-section').firstChild);
                
                // Remove alert after 3 seconds
                setTimeout(() => {
                    alert.remove();
                }, 3000);
            }, 2000);
        }

        // Planet icon hover effects
        document.querySelectorAll('.planet-icon').forEach(icon => {
            icon.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px) scale(1.1)';
            });
            
            icon.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Market status update
        function updateMarketStatus() {
            const now = new Date();
            const hour = now.getHours();
            const minute = now.getMinutes();
            const timeInMinutes = hour * 60 + minute;
            
            const marketOpen = 9 * 60 + 15; // 9:15 AM
            const marketClose = 15 * 60 + 15; // 3:15 PM
            
            const statusIndicator = document.querySelector('.status-indicator');
            
            if (timeInMinutes >= marketOpen && timeInMinutes <= marketClose) {
                statusIndicator.textContent = 'Market Open';
                statusIndicator.style.color = '#4caf50';
                statusIndicator.style.fontWeight = 'bold';
            } else {
                statusIndicator.textContent = 'Market Closed';
                statusIndicator.style.color = '#f44336';
                statusIndicator.style.fontWeight = 'bold';
            }
        }

        // Update market status on page load
        updateMarketStatus();
        
        // Update market status every minute
        setInterval(updateMarketStatus, 60000);

        // Add smooth scrolling for internal links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });

        // Add keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                generateReport();
            }
        });
    </script>
</body>
</html>
