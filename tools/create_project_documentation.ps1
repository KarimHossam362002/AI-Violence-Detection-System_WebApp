$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Out = Join-Path $Root "AI Violence Detection System Documentation.docx"
$PdfOut = Join-Path $Root "AI Violence Detection System Documentation.pdf"
$Diagram = Join-Path $Root "documentation_architecture.png"

function New-ArchitectureDiagram {
    Add-Type -AssemblyName System.Drawing
    $bmp = New-Object System.Drawing.Bitmap 1700, 760
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $white = [System.Drawing.Brushes]::White
    $blue = [System.Drawing.Color]::FromArgb(23,54,93)
    $gold = [System.Drawing.Color]::FromArgb(197,146,42)
    $lightBlue = [System.Drawing.Color]::FromArgb(217,234,247)
    $lightGold = [System.Drawing.Color]::FromArgb(248,233,192)
    $g.FillRectangle($white, 0, 0, 1700, 760)
    $g.FillRectangle((New-Object System.Drawing.SolidBrush $blue), 0, 0, 1700, 90)
    $titleFont = New-Object System.Drawing.Font "Arial", 34, ([System.Drawing.FontStyle]::Bold)
    $boxFont = New-Object System.Drawing.Font "Arial", 24, ([System.Drawing.FontStyle]::Bold)
    $smallFont = New-Object System.Drawing.Font "Arial", 18
    $g.DrawString("High-Level Architecture of the AI Violence Detection System", $titleFont, [System.Drawing.Brushes]::White, 40, 24)

    function Draw-Box($x, $y, $w, $h, $title, $desc) {
        $rect = New-Object System.Drawing.Rectangle $x, $y, $w, $h
        $path = New-Object System.Drawing.Drawing2D.GraphicsPath
        $r = 22
        $path.AddArc($x, $y, $r, $r, 180, 90)
        $path.AddArc($x + $w - $r, $y, $r, $r, 270, 90)
        $path.AddArc($x + $w - $r, $y + $h - $r, $r, $r, 0, 90)
        $path.AddArc($x, $y + $h - $r, $r, $r, 90, 90)
        $path.CloseFigure()
        $g.FillPath((New-Object System.Drawing.SolidBrush $lightBlue), $path)
        $g.DrawPath((New-Object System.Drawing.Pen $blue, 4), $path)
        $sf = New-Object System.Drawing.StringFormat
        $sf.Alignment = [System.Drawing.StringAlignment]::Center
        $sf.LineAlignment = [System.Drawing.StringAlignment]::Center
        $g.DrawString($title, $boxFont, (New-Object System.Drawing.SolidBrush $blue), (New-Object System.Drawing.RectangleF $x, ($y + 18), $w, 62), $sf)
        $g.DrawString($desc, $smallFont, [System.Drawing.Brushes]::Black, (New-Object System.Drawing.RectangleF ($x + 18), ($y + 92), ($w - 36), 55), $sf)
    }

    Draw-Box 70 185 260 150 "CCTV / Camera`nSources" "Live video frames from monitored areas"
    Draw-Box 430 130 330 150 "Weapon AI Service" "OpenCV + YOLO model`nDetects visible weapons"
    Draw-Box 430 390 330 150 "Violence AI Service" "OpenCV + Keras model`nClassifies violent activity"
    Draw-Box 880 250 300 170 "Laravel Backend`n+ MySQL" "Stores cameras, incidents,`nalerts, snapshots, clips"
    Draw-Box 1320 250 305 170 "React Operator`nDashboard" "Live stream, incidents,`nevidence, reports"

    function Draw-Arrow($x1, $y1, $x2, $y2, $label, $lx, $ly) {
        $pen = New-Object System.Drawing.Pen $gold, 6
        $g.DrawLine($pen, $x1, $y1, $x2, $y2)
        $brush = New-Object System.Drawing.SolidBrush $gold
        $pts = @(
            (New-Object System.Drawing.Point $x2, $y2),
            (New-Object System.Drawing.Point ($x2 - 24), ($y2 - 13)),
            (New-Object System.Drawing.Point ($x2 - 24), ($y2 + 13))
        )
        $g.FillPolygon($brush, $pts)
        $g.DrawString($label, $smallFont, (New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(90,70,20))), $lx, $ly)
    }
    Draw-Arrow 330 255 430 205 "Frames" 345 204
    Draw-Arrow 330 255 430 465 "Frames" 345 455
    Draw-Arrow 760 205 880 300 "POST incidents" 770 235
    Draw-Arrow 760 465 880 370 "POST incidents" 770 455
    Draw-Arrow 1180 335 1320 335 "Review and respond" 1195 302
    $g.FillRectangle((New-Object System.Drawing.SolidBrush $lightGold), 70, 630, 1555, 70)
    $g.DrawRectangle((New-Object System.Drawing.Pen $gold, 2), 70, 630, 1555, 70)
    $g.DrawString("Evidence flow: detected event -> confidence/alert level -> snapshot and video clip -> stored incident record -> operator inspection.", $smallFont, [System.Drawing.Brushes]::Black, 95, 652)
    $bmp.Save($Diagram, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose()
    $bmp.Dispose()
}

function Set-BaseFormatting($selection) {
    $selection.Font.Name = "Arial"
    $selection.Font.Size = 12
    $selection.ParagraphFormat.LineSpacingRule = 0
    $selection.ParagraphFormat.SpaceAfter = 8
    $selection.ParagraphFormat.FirstLineIndent = 18
}

function Add-Para($selection, [string]$text) {
    $selection.Style = "Normal"
    Set-BaseFormatting $selection
    $selection.TypeText($text)
    $selection.TypeParagraph()
}

function Add-Heading($selection, [string]$text, [int]$level) {
    $selection.Style = "Heading $level"
    $selection.Font.Name = "Arial"
    $selection.Font.Bold = $true
    if ($level -eq 1) { $selection.Font.Size = 16 } elseif ($level -eq 2) { $selection.Font.Size = 14 } else { $selection.Font.Size = 12 }
    $selection.Font.Color = 0x5D3617
    $selection.ParagraphFormat.FirstLineIndent = 0
    $selection.ParagraphFormat.SpaceBefore = 12
    $selection.ParagraphFormat.SpaceAfter = 6
    $selection.TypeText($text)
    $selection.TypeParagraph()
    Set-BaseFormatting $selection
}

function Add-Bullets($selection, [string[]]$items) {
    foreach ($item in $items) {
        $selection.Style = "Normal"
        $selection.Range.ListFormat.ApplyBulletDefault()
        $selection.TypeText($item)
        $selection.TypeParagraph()
        $selection.Range.ListFormat.RemoveNumbers()
    }
}

function Add-Numbers($selection, [string[]]$items) {
    foreach ($item in $items) {
        $selection.Style = "Normal"
        $selection.Range.ListFormat.ApplyNumberDefault()
        $selection.TypeText($item)
        $selection.TypeParagraph()
        $selection.Range.ListFormat.RemoveNumbers()
    }
}

function Add-SimpleTable($doc, $selection, [string[]]$headers, [object[]]$rows) {
    $range = $selection.Range
    $table = $doc.Tables.Add($range, $rows.Count + 1, $headers.Count)
    $table.Style = "Table Grid"
    $table.Range.Font.Name = "Arial"
    $table.Range.Font.Size = 10.5
    $table.Rows.Item(1).Range.Bold = $true
    $table.Rows.Item(1).Shading.BackgroundPatternColor = 15773696
    for ($c = 1; $c -le $headers.Count; $c++) {
        $table.Cell(1, $c).Range.Text = $headers[$c - 1]
    }
    for ($r = 0; $r -lt $rows.Count; $r++) {
        for ($c = 0; $c -lt $headers.Count; $c++) {
            $table.Cell($r + 2, $c + 1).Range.Text = [string]$rows[$r][$c]
        }
    }
    $table.AutoFitBehavior(1)
    $selection.SetRange($table.Range.End, $table.Range.End)
    $selection.TypeParagraph()
}

function Add-Caption($selection, [string]$text) {
    $selection.Style = "Caption"
    $selection.ParagraphFormat.Alignment = 1
    $selection.TypeText($text)
    $selection.TypeParagraph()
    $selection.ParagraphFormat.Alignment = 0
}

New-ArchitectureDiagram

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Add()
$selection = $word.Selection
$doc.PageSetup.TopMargin = 72
$doc.PageSetup.BottomMargin = 72
$doc.PageSetup.LeftMargin = 72
$doc.PageSetup.RightMargin = 72

$doc.Styles.Item("Normal").Font.Name = "Arial"
$doc.Styles.Item("Normal").Font.Size = 12
$doc.Styles.Item("Normal").ParagraphFormat.SpaceAfter = 8
$doc.Styles.Item("Normal").ParagraphFormat.FirstLineIndent = 18

$selection.ParagraphFormat.Alignment = 1
$selection.Font.Name = "Arial"
$selection.Font.Bold = $true
$selection.Font.Size = 14
$selection.Font.Color = 0x5D3617
$selection.TypeText("Ain Shams University`vFaculty of Computer and Information Sciences`vComputer Systems Department")
$selection.TypeParagraph()
$selection.TypeParagraph()
$selection.Font.Size = 28
$selection.TypeText("AI Violence Detection System")
$selection.TypeParagraph()
$selection.Font.Size = 16
$selection.Font.Color = 0x2A92C5
$selection.TypeText("Graduation Project Documentation")
$selection.TypeParagraph()
$selection.TypeParagraph()
$selection.ParagraphFormat.Alignment = 0
Add-SimpleTable $doc $selection @("Item", "Details") @(
    @("Project Area", "Artificial Intelligence, Computer Vision, Public Safety, and Web Monitoring Systems"),
    @("Project Scope", "Real-time violence and weapon detection from camera streams with incident recording and dashboard review"),
    @("Academic Year", "2025/2026")
)
$selection.ParagraphFormat.Alignment = 1
$selection.Font.Size = 12
$selection.Font.Bold = $true
$selection.TypeText("Prepared by`vProject Team Members")
$selection.InsertBreak(7)

Add-Heading $selection "Internal Cover Page" 1
Add-SimpleTable $doc $selection @("Field", "Information") @(
    @("University", "Ain Shams University"),
    @("Faculty", "Faculty of Computer and Information Sciences"),
    @("Department", "Computer Systems Department"),
    @("Project Title", "AI Violence Detection System"),
    @("Submitted By", "Project Team Members"),
    @("Supervisor", "Project Supervisor"),
    @("Year", "2025/2026")
)
$selection.InsertBreak(7)

Add-Heading $selection "Acknowledgement" 1
Add-Para $selection "We would like to express our sincere gratitude to our supervisor, faculty members, teaching assistants, and everyone who supported this graduation project. Their guidance helped us connect artificial intelligence concepts with a practical public-safety application. We also thank our families and colleagues for their encouragement throughout the design, implementation, and testing phases."
$selection.InsertBreak(7)

Add-Heading $selection "Abstract" 1
Add-Para $selection "Violence and weapon-related incidents can escalate within seconds, especially in crowded public places, transportation areas, campuses, commercial zones, and sensitive facilities. Traditional surveillance depends mainly on continuous human observation, which becomes difficult when many camera feeds must be monitored at the same time. The AI Violence Detection System addresses this problem by using computer vision to analyze camera streams, detect violent behavior or weapons, record evidence, and notify operators through a centralized web dashboard."
Add-Para $selection "The project is motivated by the need to support safer communities locally across Egypt and globally wherever camera-based monitoring is used. The system does not replace law-enforcement judgment; instead, it provides faster awareness, organized evidence, and a structured incident workflow that can help prevent criminal actions from developing unnoticed. The proposed solution combines Python/OpenCV AI services, a YOLO-based weapon detection model, a Keras-based violence classification model, a Laravel backend, a MySQL database, and a React dashboard."
Add-Para $selection "The solution demonstrates how local camera sources can be connected to AI analysis services that generate incident records with confidence scores, alert levels, snapshots, and video clips. Operators can inspect incidents, review camera information, and use stored evidence for response and reporting. The system is evaluated through functional testing of stream access, incident submission, dashboard display, evidence storage, and alert classification."
$selection.InsertBreak(7)

Add-Heading $selection "Table of Contents" 1
$tocRange = $selection.Range
$doc.TablesOfContents.Add($tocRange, $true, 1, 3) | Out-Null
$selection.EndKey(6) | Out-Null
$selection.InsertBreak(7)

Add-Heading $selection "List of Figures" 1
$tofRange = $selection.Range
$doc.TablesOfFigures.Add($tofRange, "Figure") | Out-Null
$selection.EndKey(6) | Out-Null
$selection.InsertBreak(7)

Add-Heading $selection "List of Tables" 1
$lotRange = $selection.Range
$doc.TablesOfFigures.Add($lotRange, "Table") | Out-Null
$selection.EndKey(6) | Out-Null
$selection.InsertBreak(7)

Add-Heading $selection "List of Abbreviations" 1
Add-SimpleTable $doc $selection @("Abbreviation", "Meaning") @(
    @("AI", "Artificial Intelligence"),
    @("API", "Application Programming Interface"),
    @("CCTV", "Closed-Circuit Television"),
    @("CNN", "Convolutional Neural Network"),
    @("CV", "Computer Vision"),
    @("HTTP", "Hypertext Transfer Protocol"),
    @("JSON", "JavaScript Object Notation"),
    @("MVC", "Model-View-Controller"),
    @("OpenCV", "Open Source Computer Vision Library"),
    @("YOLO", "You Only Look Once object detection model family")
)
$selection.InsertBreak(7)

Add-Heading $selection "Chapter 1: Introduction" 1
Add-Heading $selection "1.1 Project Area" 2
Add-Para $selection "The project belongs to the areas of artificial intelligence, computer vision, public-safety systems, and web-based monitoring dashboards. Computer vision allows software to interpret visual information from images and video frames. In the context of surveillance, it can help detect patterns that may indicate risk, such as aggressive physical actions or visible weapons."
Add-Para $selection "Many organizations already use cameras for security, but the value of these cameras depends on the ability to observe and interpret feeds at the right time. When many streams are active, human operators may miss short or unexpected events. AI-assisted monitoring can reduce this delay by analyzing frames continuously and raising an alert when suspicious activity is detected."
Add-Heading $selection "1.2 Project Motivation" 2
Add-Para $selection "The main motivation of this project is to contribute to violence prevention and crime reduction through early detection. Locally, Egypt has many crowded environments such as universities, metro stations, streets, malls, hospitals, and public-service buildings where rapid awareness of violent behavior can help protect citizens and support security teams. A system that highlights risky events quickly can help operators respond before an incident becomes more dangerous."
Add-Para $selection "Globally, the same need exists in many countries and communities. Violence, weapon threats, and criminal actions are not limited to one region; they are public-safety challenges that require faster information, better monitoring, and reliable evidence. This project is therefore designed as a locally useful and globally relevant system: it can be adapted to different camera sources, locations, and operational policies."
Add-Para $selection "The project is also motivated by the practical limitations of manual surveillance. A human operator can become tired, distracted, or overloaded when watching several feeds for long periods. AI can assist by continuously scanning frames, detecting high-risk patterns, and organizing the resulting evidence. This improves situational awareness while keeping final decisions in the hands of authorized people."
Add-Heading $selection "1.3 Problem Definition" 2
Add-Para $selection "Security teams often depend on live CCTV monitoring to discover violent incidents or weapon threats. However, manual monitoring is slow, difficult to scale, and vulnerable to missed events. A violent action may happen in a few seconds, and if the operator does not notice it immediately, the opportunity for early intervention may be lost."
Add-Para $selection "The problem addressed by this project is the absence of an integrated system that can analyze camera streams in real time, detect violence or weapons, classify the seriousness of the event, save related evidence, and present the incident clearly to an operator. Without this integration, camera feeds, AI results, evidence files, and incident records may remain disconnected, making response and investigation less efficient."
Add-Para $selection "Therefore, the project focuses on building a practical AI-supported monitoring platform that receives live frames, applies detection models, sends incident data to a backend API, stores evidence, and displays alerts through a dashboard. The goal is to reduce detection delay and improve the organization of information needed to prevent violent and criminal actions."
Add-Heading $selection "1.4 Project Objectives" 2
Add-Numbers $selection @(
    "Develop an AI-assisted system capable of detecting violence and weapon-related threats from camera streams.",
    "Support local public-safety needs in Egypt while keeping the design adaptable for global deployment contexts.",
    "Provide a web dashboard where operators can monitor incidents, cameras, alert levels, evidence, and recent trends.",
    "Store incident data in a structured database with related confidence scores, timestamps, camera identifiers, districts, snapshots, and video clips.",
    "Integrate separate AI services with a Laravel backend using clear API communication.",
    "Reduce the dependency on continuous manual observation by automatically highlighting suspicious events.",
    "Create a documentation structure that explains the problem, motivation, design, implementation, testing, conclusion, and future work clearly."
)
Add-Heading $selection "1.5 System Description and Main Phases" 2
Add-Para $selection "The AI Violence Detection System is composed of camera sources, Python AI services, a backend API, persistent storage, and an operator dashboard. Each part has a specific role in the detection and response workflow."
$selection.ParagraphFormat.Alignment = 1
$selection.InlineShapes.AddPicture($Diagram) | Out-Null
$selection.TypeParagraph()
Add-Caption $selection "Figure 1.1: High-level architecture of the AI Violence Detection System"
$selection.ParagraphFormat.Alignment = 0
Add-Heading $selection "1.5.1 Camera Input Phase" 3
Add-Para $selection "The system starts with camera or CCTV sources. In the current implementation, the AI services can use local camera sources during development. These sources provide frames that are read through OpenCV and prepared for analysis."
Add-Heading $selection "1.5.2 AI Analysis Phase" 3
Add-Para $selection "Two AI services analyze the incoming frames. The weapon detection service uses a YOLO model to identify visible weapons, while the violence detection service uses a Keras model to classify violent activity. Each service exposes stream and control endpoints and can generate an incident when the detection threshold is reached."
Add-Heading $selection "1.5.3 Incident Recording Phase" 3
Add-Para $selection "When a suspicious event is detected, the AI service prepares an incident payload that includes camera ID, district, event type, confidence, violence score when available, weapon flag, alert level, snapshot path, clip path, and metadata. This payload is sent to the Laravel API endpoint for storage."
Add-Heading $selection "1.5.4 Backend and Database Phase" 3
Add-Para $selection "The Laravel backend receives incident requests, validates the data, creates or updates camera records, stores incident records in MySQL, and exposes web pages for dashboard, stream, cameras, incidents, evidence, and reports."
Add-Heading $selection "1.5.5 Operator Dashboard Phase" 3
Add-Para $selection "The React dashboard presents recent incidents, alert levels, registered cameras, evidence links, and trend information. It allows an operator to inspect incidents quickly and review snapshots or video clips."
Add-Heading $selection "1.6 Documentation Organization" 2
Add-Para $selection "The rest of this documentation is organized as follows:"
Add-Bullets $selection @(
    "Chapter 2 presents the background and related work for computer vision, violence detection, weapon detection, and security monitoring systems.",
    "Chapter 3 explains the proposed system architecture and design decisions.",
    "Chapter 4 describes implementation details for the backend, frontend dashboard, AI services, API integration, and evidence storage.",
    "Chapter 5 discusses testing methodology, test cases, and expected results.",
    "Chapter 6 presents the conclusion and possible future work.",
    "Appendix A provides a user manual for running and using the system.",
    "Appendix B lists references used to support the documentation."
)
$selection.InsertBreak(7)

Add-Heading $selection "Chapter 2: Background and Related Work" 1
Add-Heading $selection "2.1 Computer Vision in Public Safety" 2
Add-Para $selection "Computer vision is widely used to extract information from visual data. In public-safety applications, it can support object detection, activity recognition, crowd analysis, and abnormal-event detection. These techniques are useful when camera networks produce more visual information than operators can comfortably monitor."
Add-Heading $selection "2.2 Violence Detection" 2
Add-Para $selection "Violence detection aims to identify physical actions that may indicate fighting, assault, or aggressive movement. Video-based methods usually analyze sequences of frames because motion over time is important for distinguishing normal actions from violent ones."
Add-Heading $selection "2.3 Weapon Detection" 2
Add-Para $selection "Weapon detection focuses on identifying dangerous objects such as guns or knives in video frames. Object-detection models such as YOLO are suitable for this task because they can localize objects and return confidence scores quickly enough for near-real-time applications."
Add-Heading $selection "2.4 Existing Monitoring Limitations" 2
Add-SimpleTable $doc $selection @("Monitoring Approach", "Advantages", "Limitations") @(
    @("Manual CCTV observation", "Simple to deploy; human judgment is available", "Hard to scale; events can be missed; operators become overloaded"),
    @("Recording-only cameras", "Provides evidence after an event", "Does not support early intervention"),
    @("AI-assisted monitoring", "Continuous analysis; faster alerts; structured evidence", "Requires model training, threshold tuning, and responsible deployment")
)
Add-Caption $selection "Table 2.1: Comparison of monitoring approaches"
$selection.InsertBreak(7)

Add-Heading $selection "Chapter 3: System Architecture and Design" 1
Add-Heading $selection "3.1 Architecture Overview" 2
Add-Para $selection "The system is designed as separated services. Laravel handles authentication, web routes, API routes, database models, and incident storage. React/Vite powers interactive dashboard screens. Python services handle the AI tasks and expose MJPEG streams and control endpoints."
Add-Heading $selection "3.2 Main System Modules" 2
Add-SimpleTable $doc $selection @("Module", "Role in the System") @(
    @("Camera Module", "Represents monitored sources and keeps camera identifiers, district data, status, and stream information."),
    @("AI Services", "Analyze frames, detect violence or weapons, save evidence, and post incidents to the backend."),
    @("Incident API", "Receives validated incident data from AI services and stores it in the database."),
    @("Dashboard", "Displays recent incidents, alert mix, trends, cameras, and evidence for operators."),
    @("Evidence Storage", "Stores snapshots and video clips under the public incident storage path.")
)
Add-Caption $selection "Table 3.1: Main system modules"
Add-Heading $selection "3.3 Data Flow" 2
Add-Para $selection "The data flow begins with a camera frame. The AI service reads the frame, applies its model, annotates the stream when needed, and checks confidence thresholds. If an incident is detected, the service saves a snapshot and clip, builds a JSON payload, and sends it to the backend. The backend stores the record and makes it visible in dashboard pages."
$selection.InsertBreak(7)

Add-Heading $selection "Chapter 4: Implementation" 1
Add-Heading $selection "4.1 Backend Implementation" 2
Add-Para $selection "The backend is implemented with Laravel. It provides web routes for dashboard pages and API routes for receiving incidents. The main models are Camera, Incident, and User. The IncidentController validates incoming data and stores the event with its alert level and evidence paths."
Add-Heading $selection "4.2 Frontend Dashboard Implementation" 2
Add-Para $selection "The frontend uses React with Vite inside the Laravel project. It provides dashboard components for incident tables, camera lists, stream controls, alert badges, and evidence links. The dashboard is designed for operators who need fast scanning and direct access to incident details."
Add-Heading $selection "4.3 AI Service Implementation" 2
Add-Para $selection "The Python AI services use OpenCV for frame capture and streaming. The weapon service loads a YOLO model and checks object-detection confidence. The violence service loads a Keras model and predicts whether recent frames indicate violent activity. Both services save snapshots and clips under the public storage incident folders."
Add-Heading $selection "4.4 API Integration" 2
Add-SimpleTable $doc $selection @("Endpoint", "Method", "Purpose") @(
    @("/api/incidents", "GET", "Return stored incidents with related camera data."),
    @("/api/incidents", "POST", "Receive new incident records from AI services."),
    @("AI service /status", "GET", "Return camera/model status for a service."),
    @("AI service /stream", "GET", "Return MJPEG stream for monitoring."),
    @("AI service /start and /stop", "POST", "Control tracking mode in the AI service.")
)
Add-Caption $selection "Table 4.1: Important system endpoints"
$selection.InsertBreak(7)

Add-Heading $selection "Chapter 5: Testing" 1
Add-Heading $selection "5.1 Testing Methodology" 2
Add-Para $selection "Testing focuses on validating the complete workflow from camera stream to dashboard display. The system should be tested module by module and then as an integrated pipeline."
Add-Heading $selection "5.2 Test Cases" 2
Add-SimpleTable $doc $selection @("Test Case", "Expected Result") @(
    @("Open the Laravel dashboard", "The login/dashboard pages load without errors."),
    @("Start an AI service", "The service returns a valid status response and stream endpoint."),
    @("Submit an incident to /api/incidents", "The backend validates and stores the incident record."),
    @("Detect a weapon event", "A critical alert is created with weapon_detected set to true."),
    @("Detect a violence event", "A high alert is created with a violence score and saved evidence."),
    @("Open incident details", "The operator can view event data, camera data, snapshot, clip, and metadata.")
)
Add-Caption $selection "Table 5.1: Functional test cases"
Add-Heading $selection "5.3 Testing Results" 2
Add-Para $selection "The expected testing result is that incidents are created correctly, evidence files are reachable through public storage, alert levels are displayed with the correct priority, and the dashboard refreshes recent incidents for operator review."
$selection.InsertBreak(7)

Add-Heading $selection "Chapter 6: Conclusion and Future Work" 1
Add-Heading $selection "6.1 Conclusion" 2
Add-Para $selection "This project presents an AI-assisted violence and weapon detection system that connects computer vision models with a practical web monitoring platform. It supports faster incident awareness, organized evidence storage, and clearer operator review. The system is especially relevant for improving public-safety monitoring in Egypt, while also being adaptable to global environments that require early detection of violent or criminal actions."
Add-Heading $selection "6.2 Future Work" 2
Add-Bullets $selection @(
    "Combine violence and weapon detection into one camera pipeline to avoid opening the same camera from multiple processes.",
    "Improve the models using larger and more diverse datasets from different lighting conditions, camera angles, and environments.",
    "Add role-based access control for different operator and administrator permissions.",
    "Add real-time notification channels such as SMS, email, or mobile push notifications.",
    "Deploy the system on edge devices or local servers near camera networks to reduce latency.",
    "Add map-based incident visualization for districts and public areas."
)
$selection.InsertBreak(7)

Add-Heading $selection "Appendix A: User Manual" 1
Add-Heading $selection "A.1 Running the Web Application" 2
Add-Numbers $selection @(
    "Install PHP and Node dependencies using composer install and npm install.",
    "Create the environment file and configure the MySQL database.",
    "Run migrations and seeders, then create the public storage link.",
    "Start the Laravel server and Vite development server.",
    "Open the login page and access the operator dashboard."
)
Add-Heading $selection "A.2 Running the AI Services" 2
Add-Numbers $selection @(
    "Install Python requirements for the AI service environment.",
    "Place the weapon and violence model files in the configured storage paths.",
    "Run the weapon detection service or the violence detection service.",
    "Check the /status endpoint to confirm that the camera is open.",
    "Use the dashboard stream page and incident pages to review detections."
)
$selection.InsertBreak(7)

Add-Heading $selection "Appendix B: References" 1
Add-Numbers $selection @(
    "Laravel Documentation, ""Laravel Web Framework Documentation"", Laravel, 2026.",
    "React Documentation, ""React User Interface Library Documentation"", Meta, 2026.",
    "OpenCV Documentation, ""Open Source Computer Vision Library"", OpenCV, 2026.",
    "Ultralytics, ""YOLO Object Detection Documentation"", Ultralytics, 2026.",
    "TensorFlow/Keras Documentation, ""Keras Deep Learning API"", Google, 2026."
)

foreach ($section in $doc.Sections) {
    $section.Headers.Item(1).Range.Text = "AI Violence Detection System"
    $section.Headers.Item(1).Range.Font.Name = "Arial"
    $section.Headers.Item(1).Range.Font.Size = 9
    $section.Footers.Item(1).PageNumbers.Add(1) | Out-Null
}

$doc.Fields.Update() | Out-Null
foreach ($toc in $doc.TablesOfContents) { $toc.Update() | Out-Null }
foreach ($tof in $doc.TablesOfFigures) { $tof.Update() | Out-Null }

if (Test-Path $Out) { Remove-Item $Out -Force }
if (Test-Path $PdfOut) { Remove-Item $PdfOut -Force }
$doc.SaveAs([ref]$Out, [ref]16)
$doc.ExportAsFixedFormat($PdfOut, 17)
$doc.Close($false)
$word.Quit()

Write-Output $Out
