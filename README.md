# SONAR Compromised Area Detection Simulation!

[SONAR Simulation Screenshot]
(sonar.png)

A Pygame simulation demonstrating SONAR technology for detecting compromised areas (mines) on the seabed. The program visualizes how SONAR pings can identify dangerous objects underwater.

## Features

- Real-time SONAR visualization with adjustable beam angle- Randomly generated seabed terrain- Minefield generation in a specified "compromised area"- Automatic and manual SONAR pinging- Persistent danger zone marking- Visual feedback for seabed and mine detections
-
- ## How It Works
-
- 1. A boat moves across the screen emitting periodic SONAR pings
  2. The SONAR beam detects both the seabed and mines
  3. Detected mines are marked as danger zones
  4. The system provides visual feedback:
     - Green: Seabed detections
     - Yellow: Mines
     - Red: Confirmed danger zones
    
   ## Controls

  - **SPACEBAR**: Manual SONAR ping- The system also auto-pings every 2 seconds

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

Clone the repository: 
```bash
git clone https://github.com/Jean6114/Sonar.git
