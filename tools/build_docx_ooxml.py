from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from html import escape
import os


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "AI Violence Detection System Documentation.docx"
IMG = ROOT / "documentation_architecture.png"


def t(text):
    return escape(text, quote=False)


def r(text, bold=False, size=None, color=None, italic=False):
    props = []
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    if size:
        props.append(f'<w:sz w:val="{size * 2}"/>')
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>" if props else ""
    return f"<w:r>{rpr}<w:t xml:space=\"preserve\">{t(text)}</w:t></w:r>"


def p(text="", style=None, align=None, page_break=False, first_indent=True, runs=None):
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    if not first_indent:
        ppr.append('<w:ind w:firstLine="0"/>')
    if ppr:
        ppr_xml = f"<w:pPr>{''.join(ppr)}</w:pPr>"
    else:
        ppr_xml = ""
    body = "".join(runs) if runs else r(text)
    if page_break:
        body += '<w:r><w:br w:type="page"/></w:r>'
    return f"<w:p>{ppr_xml}{body}</w:p>"


def heading(text, level=1):
    return p(text, style=f"Heading{level}", first_indent=False)


def bullet(text):
    return (
        '<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr>'
        '<w:ind w:left="720" w:hanging="360"/></w:pPr>'
        f"{r(text)}</w:p>"
    )


def numbered(text):
    return (
        '<w:p><w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="1"/></w:numPr>'
        '<w:ind w:left="720" w:hanging="360"/></w:pPr>'
        f"{r(text)}</w:p>"
    )


def caption(text):
    return p(text, style="Caption", align="center", first_indent=False)


def page_break():
    return p("", page_break=True)


def table(headers, rows):
    cols = len(headers)
    grid = "".join('<w:gridCol w:w="3000"/>' for _ in range(cols))
    out = [
        '<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="9360" w:type="dxa"/>'
        '<w:tblLook w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
        "</w:tblPr><w:tblGrid>",
        grid,
        "</w:tblGrid>",
    ]

    def cell(text, header=False):
        shade = '<w:shd w:fill="D9EAF7"/>' if header else ""
        return (
            '<w:tc><w:tcPr><w:tcW w:w="3000" w:type="dxa"/>'
            f"{shade}<w:tcMar><w:top w:w=\"120\" w:type=\"dxa\"/><w:left w:w=\"120\" w:type=\"dxa\"/>"
            '<w:bottom w:w="120" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tcMar></w:tcPr>'
            f"{p(text, first_indent=False, runs=[r(text, bold=header, color='17365D' if header else None, size=10)])}</w:tc>"
        )

    out.append("<w:tr>" + "".join(cell(h, True) for h in headers) + "</w:tr>")
    for row in rows:
        out.append("<w:tr>" + "".join(cell(str(v)) for v in row) + "</w:tr>")
    out.append("</w:tbl>")
    return "".join(out) + p("")


def image_paragraph():
    if not IMG.exists():
        return ""
    return (
        '<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        '<wp:extent cx="5486400" cy="2453647"/><wp:docPr id="1" name="Architecture Diagram"/>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"><pic:nvPicPr><pic:cNvPr id="1" name="documentation_architecture.png"/>'
        '<pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rIdImage1" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
        '<a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="5486400" cy="2453647"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
        '</wp:inline></w:drawing></w:r></w:p>'
    )


def toc_field():
    return (
        '<w:p><w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r><w:instrText xml:space="preserve">TOC \\o "1-3" \\h \\z \\u</w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        f'{r("Right-click this table in Microsoft Word and choose Update Field to refresh page numbers.", italic=True, size=10)}'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
    )


def document_xml():
    parts = []
    parts += [
        p("Ain Shams University\nFaculty of Computer and Information Sciences\nComputer Systems Department", align="center", first_indent=False, runs=[r("Ain Shams University\nFaculty of Computer and Information Sciences\nComputer Systems Department", bold=True, size=14, color="17365D")]),
        p("AI Violence Detection System", align="center", first_indent=False, runs=[r("AI Violence Detection System", bold=True, size=28, color="17365D")]),
        p("Graduation Project Documentation", align="center", first_indent=False, runs=[r("Graduation Project Documentation", bold=True, size=16, color="C5922A")]),
        table(["Item", "Details"], [
            ["Project Area", "Artificial Intelligence, Computer Vision, Public Safety, and Web Monitoring Systems"],
            ["Project Scope", "Real-time violence and weapon detection from camera streams with incident recording and dashboard review"],
            ["Academic Year", "2025/2026"],
        ]),
        p("Prepared by\nProject Team Members", align="center", first_indent=False, runs=[r("Prepared by\nProject Team Members", bold=True)]),
        page_break(),
        heading("Internal Cover Page"),
        table(["Field", "Information"], [
            ["University", "Ain Shams University"],
            ["Faculty", "Faculty of Computer and Information Sciences"],
            ["Department", "Computer Systems Department"],
            ["Project Title", "AI Violence Detection System"],
            ["Submitted By", "Project Team Members"],
            ["Supervisor", "Project Supervisor"],
            ["Year", "2025/2026"],
        ]),
        page_break(),
        heading("Acknowledgement"),
        p("We would like to express our sincere gratitude to our supervisor, faculty members, teaching assistants, and everyone who supported this graduation project. Their guidance helped us connect artificial intelligence concepts with a practical public-safety application. We also thank our families and colleagues for their encouragement throughout the design, implementation, and testing phases."),
        page_break(),
        heading("Abstract"),
        p("Violence and weapon-related incidents can escalate within seconds, especially in crowded public places, transportation areas, campuses, commercial zones, and sensitive facilities. Traditional surveillance depends mainly on continuous human observation, which becomes difficult when many camera feeds must be monitored at the same time. The AI Violence Detection System addresses this problem by using computer vision to analyze camera streams, detect violent behavior or weapons, record evidence, and notify operators through a centralized web dashboard."),
        p("The project is motivated by the need to support safer communities locally across Egypt and globally wherever camera-based monitoring is used. The system does not replace law-enforcement judgment; instead, it provides faster awareness, organized evidence, and a structured incident workflow that can help prevent criminal actions from developing unnoticed. The proposed solution combines Python/OpenCV AI services, a YOLO-based weapon detection model, a Keras-based violence classification model, a Laravel backend, a MySQL database, a React dashboard, and a Docker-based runtime for the web stack."),
        p("The solution demonstrates how local camera sources can be connected to AI analysis services that generate incident records with confidence scores, alert levels, snapshots, and video clips. Operators can inspect incidents, review camera information, and use stored evidence for response and reporting. The system is evaluated through functional testing of stream access, incident submission, dashboard display, evidence storage, and alert classification."),
        page_break(),
        heading("Table of Contents"),
        toc_field(),
        page_break(),
        heading("List of Figures"),
        p("Figure 1.1: High-level architecture of the AI Violence Detection System", first_indent=False),
        page_break(),
        heading("List of Tables"),
        p("Table 2.1: Comparison of monitoring approaches", first_indent=False),
        p("Table 3.1: Main system modules", first_indent=False),
        p("Table 4.1: Docker containers used by the project", first_indent=False),
        p("Table 4.2: Important system endpoints", first_indent=False),
        p("Table 5.1: Functional test cases", first_indent=False),
        page_break(),
        heading("List of Abbreviations"),
        table(["Abbreviation", "Meaning"], [
            ["AI", "Artificial Intelligence"], ["API", "Application Programming Interface"], ["CCTV", "Closed-Circuit Television"],
            ["CNN", "Convolutional Neural Network"], ["CV", "Computer Vision"], ["HTTP", "Hypertext Transfer Protocol"],
            ["JSON", "JavaScript Object Notation"], ["MVC", "Model-View-Controller"], ["OpenCV", "Open Source Computer Vision Library"], ["YOLO", "You Only Look Once object detection model family"],
        ]),
        page_break(),
        heading("Chapter 1: Introduction"),
        heading("1.1 Project Area", 2),
        p("The project belongs to the areas of artificial intelligence, computer vision, public-safety systems, and web-based monitoring dashboards. Computer vision allows software to interpret visual information from images and video frames. In the context of surveillance, it can help detect patterns that may indicate risk, such as aggressive physical actions or visible weapons."),
        p("Many organizations already use cameras for security, but the value of these cameras depends on the ability to observe and interpret feeds at the right time. When many streams are active, human operators may miss short or unexpected events. AI-assisted monitoring can reduce this delay by analyzing frames continuously and raising an alert when suspicious activity is detected."),
        heading("1.2 Project Motivation", 2),
        p("The main motivation of this project is to contribute to violence prevention and crime reduction through early detection. Locally, Egypt has many crowded environments such as universities, metro stations, streets, malls, hospitals, and public-service buildings where rapid awareness of violent behavior can help protect citizens and support security teams. A system that highlights risky events quickly can help operators respond before an incident becomes more dangerous."),
        p("Globally, the same need exists in many countries and communities. Violence, weapon threats, and criminal actions are not limited to one region; they are public-safety challenges that require faster information, better monitoring, and reliable evidence. This project is therefore designed as a locally useful and globally relevant system: it can be adapted to different camera sources, locations, and operational policies."),
        p("The project is also motivated by the practical limitations of manual surveillance. A human operator can become tired, distracted, or overloaded when watching several feeds for long periods. AI can assist by continuously scanning frames, detecting high-risk patterns, and organizing the resulting evidence. This improves situational awareness while keeping final decisions in the hands of authorized people."),
        heading("1.3 Problem Definition", 2),
        p("Security teams often depend on live CCTV monitoring to discover violent incidents or weapon threats. However, manual monitoring is slow, difficult to scale, and vulnerable to missed events. A violent action may happen in a few seconds, and if the operator does not notice it immediately, the opportunity for early intervention may be lost."),
        p("The problem addressed by this project is the absence of an integrated system that can analyze camera streams in real time, detect violence or weapons, classify the seriousness of the event, save related evidence, and present the incident clearly to an operator. Without this integration, camera feeds, AI results, evidence files, and incident records may remain disconnected, making response and investigation less efficient."),
        p("Therefore, the project focuses on building a practical AI-supported monitoring platform that receives live frames, applies detection models, sends incident data to a backend API, stores evidence, and displays alerts through a dashboard. The goal is to reduce detection delay and improve the organization of information needed to prevent violent and criminal actions."),
        heading("1.4 Project Objectives", 2),
        numbered("Develop an AI-assisted system capable of detecting violence and weapon-related threats from camera streams."),
        numbered("Support local public-safety needs in Egypt while keeping the design adaptable for global deployment contexts."),
        numbered("Provide a web dashboard where operators can monitor incidents, cameras, alert levels, evidence, and recent trends."),
        numbered("Store incident data in a structured database with related confidence scores, timestamps, camera identifiers, districts, snapshots, and video clips."),
        numbered("Integrate separate AI services with a Laravel backend using clear API communication."),
        numbered("Reduce the dependency on continuous manual observation by automatically highlighting suspicious events."),
        numbered("Create a documentation structure that explains the problem, motivation, design, implementation, testing, conclusion, and future work clearly."),
        heading("1.5 System Description and Main Phases", 2),
        p("The AI Violence Detection System is composed of camera sources, Python AI services, a backend API, persistent storage, and an operator dashboard. Each part has a specific role in the detection and response workflow."),
        image_paragraph(),
        caption("Figure 1.1: High-level architecture of the AI Violence Detection System"),
        heading("1.5.1 Camera Input Phase", 3),
        p("The system starts with camera or CCTV sources. In the current implementation, the AI services can use local camera sources during development. These sources provide frames that are read through OpenCV and prepared for analysis."),
        heading("1.5.2 AI Analysis Phase", 3),
        p("Two AI services analyze the incoming frames. The weapon detection service uses a YOLO model to identify visible weapons, while the violence detection service uses a Keras model to classify violent activity. Each service exposes stream and control endpoints and can generate an incident when the detection threshold is reached."),
        heading("1.5.3 Incident Recording Phase", 3),
        p("When a suspicious event is detected, the AI service prepares an incident payload that includes camera ID, district, event type, confidence, violence score when available, weapon flag, alert level, snapshot path, clip path, and metadata. This payload is sent to the Laravel API endpoint for storage."),
        heading("1.5.4 Backend and Database Phase", 3),
        p("The Laravel backend receives incident requests, validates the data, creates or updates camera records, stores incident records in MySQL, and exposes web pages for dashboard, stream, cameras, incidents, evidence, and reports."),
        heading("1.5.5 Operator Dashboard Phase", 3),
        p("The React dashboard presents recent incidents, alert levels, registered cameras, evidence links, and trend information. It allows an operator to inspect incidents quickly and review snapshots or video clips."),
        heading("1.6 Documentation Organization", 2),
        p("The rest of this documentation is organized as follows:"),
        bullet("Chapter 2 presents the background and related work for computer vision, violence detection, weapon detection, and security monitoring systems."),
        bullet("Chapter 3 explains the proposed system architecture and design decisions."),
        bullet("Chapter 4 describes implementation details for the backend, frontend dashboard, AI services, API integration, and evidence storage."),
        bullet("Chapter 5 discusses testing methodology, test cases, and expected results."),
        bullet("Chapter 6 presents the conclusion and possible future work."),
        bullet("Appendix A provides a user manual for running and using the system."),
        bullet("Appendix B lists references used to support the documentation."),
        page_break(),
        heading("Chapter 2: Background and Related Work"),
        heading("2.1 Computer Vision in Public Safety", 2),
        p("Computer vision is widely used to extract information from visual data. In public-safety applications, it can support object detection, activity recognition, crowd analysis, and abnormal-event detection. These techniques are useful when camera networks produce more visual information than operators can comfortably monitor."),
        heading("2.2 Violence Detection", 2),
        p("Violence detection aims to identify physical actions that may indicate fighting, assault, or aggressive movement. Video-based methods usually analyze sequences of frames because motion over time is important for distinguishing normal actions from violent ones."),
        heading("2.3 Weapon Detection", 2),
        p("Weapon detection focuses on identifying dangerous objects such as guns or knives in video frames. Object-detection models such as YOLO are suitable for this task because they can localize objects and return confidence scores quickly enough for near-real-time applications."),
        heading("2.4 Existing Monitoring Limitations", 2),
        table(["Monitoring Approach", "Advantages", "Limitations"], [
            ["Manual CCTV observation", "Simple to deploy; human judgment is available", "Hard to scale; events can be missed; operators become overloaded"],
            ["Recording-only cameras", "Provides evidence after an event", "Does not support early intervention"],
            ["AI-assisted monitoring", "Continuous analysis; faster alerts; structured evidence", "Requires model training, threshold tuning, and responsible deployment"],
        ]),
        caption("Table 2.1: Comparison of monitoring approaches"),
        page_break(),
        heading("Chapter 3: System Architecture and Design"),
        heading("3.1 Architecture Overview", 2),
        p("The system is designed as separated services and is run mainly through Docker during development. Docker Compose starts the MySQL database, the Laravel PHP-FPM backend, the Nginx web server, and the Vite frontend server. Laravel handles authentication, web routes, API routes, database models, and incident storage. React/Vite powers interactive dashboard screens. Python services handle the AI tasks and expose MJPEG streams and control endpoints."),
        heading("3.2 Main System Modules", 2),
        table(["Module", "Role in the System"], [
            ["Camera Module", "Represents monitored sources and keeps camera identifiers, district data, status, and stream information."],
            ["AI Services", "Analyze frames, detect violence or weapons, save evidence, and post incidents to the backend."],
            ["Incident API", "Receives validated incident data from AI services and stores it in the database."],
            ["Dashboard", "Displays recent incidents, alert mix, trends, cameras, and evidence for operators."],
            ["Evidence Storage", "Stores snapshots and video clips under the public incident storage path."],
        ]),
        caption("Table 3.1: Main system modules"),
        heading("3.3 Data Flow", 2),
        p("The data flow begins with a camera frame. The AI service reads the frame, applies its model, annotates the stream when needed, and checks confidence thresholds. If an incident is detected, the service saves a snapshot and clip, builds a JSON payload, and sends it to the backend. The backend stores the record and makes it visible in dashboard pages."),
        page_break(),
        heading("Chapter 4: Implementation"),
        heading("4.1 Backend Implementation", 2),
        p("The backend is implemented with Laravel and is containerized using docker/backend/Dockerfile. The Docker image is based on PHP 8.3 FPM, installs the required PHP extensions, installs Composer dependencies, prepares Laravel storage folders, and exposes PHP-FPM to the Nginx container. The backend provides web routes for dashboard pages and API routes for receiving incidents. The main models are Camera, Incident, and User. The IncidentController validates incoming data and stores the event with its alert level and evidence paths."),
        heading("4.2 Frontend Dashboard Implementation", 2),
        p("The frontend uses React with Vite inside the Laravel project and is containerized using docker/frontend/Dockerfile. The frontend container uses Node 22 Alpine, installs npm packages, mounts the project source, and runs the Vite development server on port 5173. It provides dashboard components for incident tables, camera lists, stream controls, alert badges, and evidence links. The dashboard is designed for operators who need fast scanning and direct access to incident details."),
        heading("4.3 AI Service Implementation", 2),
        p("The Python AI services use OpenCV for frame capture and streaming. The repository includes docker/ai/Dockerfile, which installs Python requirements and system libraries such as ffmpeg, libglib, libgl, and libgomp. The weapon service loads a YOLO model and checks object-detection confidence. The violence service loads a Keras model and predicts whether recent frames indicate violent activity. Both services save snapshots and clips under the public storage incident folders."),
        heading("4.4 Docker Runtime Implementation", 2),
        p("The main development runtime is defined in docker-compose.yml. It creates four main containers: violence-mysql for MySQL 8.4, violence-backend for Laravel PHP-FPM, violence-nginx for serving the Laravel public folder on port 8000, and violence-frontend for Vite on port 5173. Named volumes are used for MySQL data, Composer cache, and node_modules. This setup allows the project to run without manually installing PHP, Composer, Node, or MySQL on the host machine."),
        table(["Container", "Purpose", "Port"],
              [["violence-mysql", "Stores application data in MySQL", "3306"],
               ["violence-backend", "Runs Laravel through PHP-FPM", "9000 internal"],
               ["violence-nginx", "Serves the web application through Nginx", "8000"],
               ["violence-frontend", "Runs the Vite development server", "5173"]]),
        caption("Table 4.1: Docker containers used by the project"),
        heading("4.5 API Integration", 2),
        table(["Endpoint", "Method", "Purpose"], [
            ["/api/incidents", "GET", "Return stored incidents with related camera data."],
            ["/api/incidents", "POST", "Receive new incident records from AI services."],
            ["AI service /status", "GET", "Return camera/model status for a service."],
            ["AI service /stream", "GET", "Return MJPEG stream for monitoring."],
            ["AI service /start and /stop", "POST", "Control tracking mode in the AI service."],
        ]),
        caption("Table 4.2: Important system endpoints"),
        page_break(),
        heading("Chapter 5: Testing"),
        heading("5.1 Testing Methodology", 2),
        p("Testing focuses on validating the complete workflow from camera stream to dashboard display. The system should be tested module by module and then as an integrated pipeline."),
        heading("5.2 Test Cases", 2),
        table(["Test Case", "Expected Result"], [
            ["Open the Laravel dashboard", "The login/dashboard pages load without errors."],
            ["Start an AI service", "The service returns a valid status response and stream endpoint."],
            ["Submit an incident to /api/incidents", "The backend validates and stores the incident record."],
            ["Detect a weapon event", "A critical alert is created with weapon_detected set to true."],
            ["Detect a violence event", "A high alert is created with a violence score and saved evidence."],
            ["Open incident details", "The operator can view event data, camera data, snapshot, clip, and metadata."],
        ]),
        caption("Table 5.1: Functional test cases"),
        heading("5.3 Testing Results", 2),
        p("The expected testing result is that incidents are created correctly, evidence files are reachable through public storage, alert levels are displayed with the correct priority, and the dashboard refreshes recent incidents for operator review."),
        page_break(),
        heading("Chapter 6: Conclusion and Future Work"),
        heading("6.1 Conclusion", 2),
        p("This project presents an AI-assisted violence and weapon detection system that connects computer vision models with a practical web monitoring platform. It supports faster incident awareness, organized evidence storage, and clearer operator review. The system is especially relevant for improving public-safety monitoring in Egypt, while also being adaptable to global environments that require early detection of violent or criminal actions."),
        heading("6.2 Future Work", 2),
        bullet("Combine violence and weapon detection into one camera pipeline to avoid opening the same camera from multiple processes."),
        bullet("Improve the models using larger and more diverse datasets from different lighting conditions, camera angles, and environments."),
        bullet("Add role-based access control for different operator and administrator permissions."),
        bullet("Add real-time notification channels such as SMS, email, or mobile push notifications."),
        bullet("Deploy the system on edge devices or local servers near camera networks to reduce latency."),
        bullet("Add map-based incident visualization for districts and public areas."),
        page_break(),
        heading("Appendix A: User Manual"),
        heading("A.1 Running the Web Application with Docker", 2),
        numbered("Install Docker Desktop and make sure the Docker engine is running."),
        numbered("Open a terminal in the project root folder that contains docker-compose.yml."),
        numbered("Create or update the environment file using the Docker database values: DB_HOST=mysql, DB_DATABASE=violence, DB_USERNAME=violence, and DB_PASSWORD=violence."),
        numbered("Run docker compose up --build. This builds and starts the MySQL, Laravel backend, Nginx, and Vite frontend containers."),
        numbered("After the containers start, open http://127.0.0.1:8000/login to access the Laravel application through Nginx."),
        numbered("Use http://127.0.0.1:5173 only as the Vite development server endpoint; the main application is served from port 8000."),
        numbered("If database tables are not created yet, run migrations inside the backend container using docker exec violence-backend php artisan migrate --seed."),
        numbered("If public evidence links are missing, run docker exec violence-backend php artisan storage:link."),
        heading("A.2 Running the AI Services", 2),
        numbered("Place the weapon model at storage/app/models/weapon/weapon_detection_yolov11m.pt and the violence model at storage/app/models/violence/cctvmodel_advanced.keras."),
        numbered("The repository includes docker/ai/Dockerfile for containerizing the Python AI environment, including ffmpeg and the required system libraries."),
        numbered("Because Docker Desktop on Windows may not pass the laptop webcam reliably into Linux containers, run the AI services directly on Windows when webcam access is required, or extend docker-compose.yml with AI service definitions when using a Linux camera source."),
        numbered("Start either ai_service/weapon_detection_service.py or ai_service/violence_detection_service.py, then check the service /status endpoint."),
        numbered("Use the dashboard stream page and incident pages to review detections, snapshots, clips, and alert levels."),
        page_break(),
        heading("Appendix B: References"),
        numbered('Laravel Documentation, "Laravel Web Framework Documentation", Laravel, 2026.'),
        numbered('React Documentation, "React User Interface Library Documentation", Meta, 2026.'),
        numbered('OpenCV Documentation, "Open Source Computer Vision Library", OpenCV, 2026.'),
        numbered('Ultralytics, "YOLO Object Detection Documentation", Ultralytics, 2026.'),
        numbered('TensorFlow/Keras Documentation, "Keras Deep Learning API", Google, 2026.'),
    ]
    body = "".join(parts)
    sect = (
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
        '<w:cols w:space="720"/><w:docGrid w:linePitch="360"/></w:sectPr>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
        'xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" '
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
        'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
        'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
        'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
        'mc:Ignorable="w14 wp14"><w:body>'
        + body
        + sect
        + "</w:body></w:document>"
    )


STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="160" w:line="276" w:lineRule="auto"/><w:ind w:firstLine="360"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:outlineLvl w:val="0"/><w:spacing w:before="240" w:after="120"/><w:ind w:firstLine="0"/></w:pPr><w:rPr><w:b/><w:color w:val="17365D"/><w:sz w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:outlineLvl w:val="1"/><w:spacing w:before="200" w:after="100"/><w:ind w:firstLine="0"/></w:pPr><w:rPr><w:b/><w:color w:val="17365D"/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:qFormat/><w:pPr><w:outlineLvl w:val="2"/><w:spacing w:before="160" w:after="80"/><w:ind w:firstLine="0"/></w:pPr><w:rPr><w:b/><w:color w:val="17365D"/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Caption"><w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:after="160"/><w:ind w:firstLine="0"/></w:pPr><w:rPr><w:i/><w:color w:val="666666"/><w:sz w:val="20"/></w:rPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:color="BFBFBF"/><w:left w:val="single" w:sz="4" w:color="BFBFBF"/><w:bottom w:val="single" w:sz="4" w:color="BFBFBF"/><w:right w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideH w:val="single" w:sz="4" w:color="BFBFBF"/><w:insideV w:val="single" w:sz="4" w:color="BFBFBF"/></w:tblBorders></w:tblPr></w:style>
</w:styles>"""

NUMBERING = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl></w:abstractNum>
<w:abstractNum w:abstractNumId="1"><w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="•"/><w:lvlJc w:val="left"/><w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr><w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/></w:rPr></w:lvl></w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num><w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>
</w:numbering>"""


def write_docx():
    if OUT.exists():
        OUT.unlink()
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Default Extension="png" ContentType="image/png"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""
    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""
    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rIdNumbering" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
<Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/documentation_architecture.png"/>
</Relationships>"""
    core = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>AI Violence Detection System Documentation</dc:title><dc:creator>Codex</dc:creator><cp:lastModifiedBy>Codex</cp:lastModifiedBy></cp:coreProperties>"""
    app = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Word</Application></Properties>"""
    with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/document.xml", document_xml())
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/numbering.xml", NUMBERING)
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)
        if IMG.exists():
            z.write(IMG, "word/media/documentation_architecture.png")
    print(OUT)
    print(os.path.getsize(OUT))


if __name__ == "__main__":
    write_docx()
