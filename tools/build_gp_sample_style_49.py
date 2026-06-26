from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_docx_ooxml import (  # noqa: E402
    ROOT, IMG, STYLES, NUMBERING, p, r, heading, bullet, numbered,
    caption, table, page_break, image_paragraph, toc_field
)

OUT = ROOT / "AI Violence Detection System Documentation - 49 Pages.docx"


def pg(*items):
    return "".join(items) + page_break()


def para_pack(title, *paras):
    content = [heading(title)]
    for text in paras:
        content.append(p(text))
    return pg(*content)


def document_xml_49():
    pages = []

    pages.append(pg(
        p("Ain Shams University\nFaculty of Computer and Information Sciences\nComputer Systems Department", align="center", first_indent=False, runs=[r("Ain Shams University\nFaculty of Computer and Information Sciences\nComputer Systems Department", bold=True, size=14, color="17365D")]),
        p("AI Violence Detection System", align="center", first_indent=False, runs=[r("AI Violence Detection System", bold=True, size=28, color="17365D")]),
        p("Graduation Project Documentation", align="center", first_indent=False, runs=[r("Graduation Project Documentation", bold=True, size=16, color="C5922A")]),
        table(["Item", "Details"], [
            ["Project Area", "Artificial Intelligence, Computer Vision, Public Safety, and Web Monitoring Systems"],
            ["Project Scope", "Real-time violence and weapon detection from camera streams with incident recording and dashboard review"],
            ["Academic Year", "2025/2026"],
        ]),
        p("Prepared by\nProject Team Members", align="center", first_indent=False, runs=[r("Prepared by\nProject Team Members", bold=True)])
    ))

    pages.append(pg(
        heading("Internal Cover Page"),
        table(["Field", "Information"], [
            ["University", "Ain Shams University"], ["Faculty", "Faculty of Computer and Information Sciences"],
            ["Department", "Computer Systems Department"], ["Project Title", "AI Violence Detection System"],
            ["Submitted By", "Project Team Members"], ["Supervisor", "Project Supervisor"], ["Year", "2025/2026"],
        ])
    ))

    pages.append(para_pack(
        "Abstract",
        "Violence and weapon-related incidents can escalate within seconds in public places, schools, universities, streets, transportation areas, and sensitive facilities. Traditional surveillance depends on human operators watching many camera streams continuously, which creates a high chance of delay or missed events. The AI Violence Detection System addresses this problem by using computer vision to analyze camera streams, detect violent behavior or visible weapons, store evidence, and show incidents in a centralized dashboard.",
        "The project is motivated by the need to support safer communities across Egypt locally and to provide a globally adaptable approach for preventing criminal actions. The system is not designed to replace human judgment or official security procedures. Instead, it assists operators by providing faster awareness, confidence scores, alert levels, snapshots, and video clips so suspicious events can be reviewed quickly.",
        "The implementation combines Laravel, React/Vite, MySQL, Docker, Nginx, Python, OpenCV, a YOLO weapon detection model, and a Keras violence detection model. The final result is a practical monitoring workflow that connects live camera analysis with incident storage and operator review."
    ))

    pages.append(pg(
        heading("Table of Contents"),
        p("Acknowledgement ........................................................................................................ i", first_indent=False),
        p("Abstract .................................................................................................................... ii", first_indent=False),
        p("List of Figures ........................................................................................................... iv", first_indent=False),
        p("List of Tables ............................................................................................................ v", first_indent=False),
        p("List of Abbreviations .............................................................................................. vi", first_indent=False),
        p("Chapter 1: Introduction ............................................................................................. 1", first_indent=False),
        p("1.1 Project Area ......................................................................................................... 1", first_indent=False),
        p("1.2 Problem Definition ............................................................................................... 2", first_indent=False),
        p("1.3 Project Motivation ............................................................................................... 3", first_indent=False),
        p("1.4 Project Objectives ............................................................................................... 4", first_indent=False),
        p("1.5 Methodology ......................................................................................................... 5", first_indent=False),
        p("1.6 Time Plan ............................................................................................................. 6", first_indent=False),
        p("1.7 Documentation Organization ............................................................................... 7", first_indent=False),
    ))

    pages.append(pg(
        heading("Table of Contents (Continued)"),
        p("Chapter 2: Literature Review ..................................................................................... 8", first_indent=False),
        p("Chapter 3: System Architecture and Methods .......................................................... 15", first_indent=False),
        p("Chapter 4: Experiment and Results ........................................................................... 23", first_indent=False),
        p("Chapter 5: Run the Application ................................................................................ 35", first_indent=False),
        p("Chapter 6: Conclusion and Future Work .................................................................. 39", first_indent=False),
        p("References .................................................................................................................. 41", first_indent=False),
        p("Appendix A: User Manual .......................................................................................... 42", first_indent=False),
        p("Appendix B: Main Source Code Locations ............................................................... 43", first_indent=False),
    ))

    pages.append(pg(
        heading("List of Figures"),
        p("Figure 1.1: High-level architecture of the AI Violence Detection System", first_indent=False),
        p("Figure 3.1: Main Docker-based system architecture", first_indent=False),
        p("Figure 4.1: Incident detection and evidence recording workflow", first_indent=False),
        p("Figure 5.1: Operator dashboard workflow", first_indent=False),
    ))

    pages.append(pg(
        heading("List of Tables"),
        p("Table 1.1: Project objectives", first_indent=False),
        p("Table 1.2: Time plan", first_indent=False),
        p("Table 2.1: Comparison of monitoring approaches", first_indent=False),
        p("Table 3.1: Main system modules", first_indent=False),
        p("Table 3.2: Docker containers used by the project", first_indent=False),
        p("Table 4.1: Important system endpoints", first_indent=False),
    ))

    pages.append(pg(
        heading("List of Abbreviations"),
        table(["Abbreviation", "Meaning"], [
            ["AI", "Artificial Intelligence"], ["API", "Application Programming Interface"], ["CCTV", "Closed-Circuit Television"],
            ["CNN", "Convolutional Neural Network"], ["CV", "Computer Vision"], ["HTTP", "Hypertext Transfer Protocol"],
            ["JSON", "JavaScript Object Notation"], ["MVC", "Model-View-Controller"], ["OpenCV", "Open Source Computer Vision Library"], ["YOLO", "You Only Look Once object detection model family"],
        ])
    ))

    pages.append(para_pack(
        "Chapter 1: Introduction",
        "The AI Violence Detection System is a graduation project in the area of artificial intelligence and public safety. It uses computer vision to help monitor camera streams and identify suspicious events that may include violent behavior or visible weapons.",
        "The project connects AI analysis services with a web application so that detection results do not remain isolated. Each incident can be stored, reviewed, and supported with evidence such as snapshots and video clips."
    ))
    pages.append(para_pack(
        "1.1 Project Area",
        "The project area includes computer vision, machine learning, object detection, activity recognition, web dashboards, and security information systems. Computer vision enables software to interpret frames from cameras and extract meaningful signals.",
        "In a public-safety context, these signals can help security teams respond faster. The project focuses on real-time or near-real-time detection rather than only recording footage for review after the event."
    ))
    pages.append(para_pack(
        "1.2 Problem Definition",
        "Security teams often rely on CCTV systems to detect violent incidents or weapon threats. However, manual monitoring becomes difficult when many camera feeds must be watched continuously. A violent action may happen quickly, and if it is missed in the first moments, the chance of early intervention is reduced.",
        "The problem addressed by this project is the lack of an integrated system that can analyze camera streams, detect violence or weapons, classify the event seriousness, save evidence, and present incidents clearly to an operator. The proposed system reduces this gap by combining AI detection, backend storage, and dashboard review."
    ))
    pages.append(para_pack(
        "1.3 Project Motivation",
        "The motivation of this project is to help prevent violence and criminal actions through earlier detection. Locally, Egypt has many crowded environments such as universities, metro stations, malls, streets, and public-service buildings where rapid awareness can protect citizens and support security teams.",
        "Globally, violence and weapon threats are shared public-safety challenges. A system that can be adapted to different camera sources and locations has value beyond one place. The project therefore aims to provide a local Egyptian safety contribution and a globally relevant monitoring approach."
    ))
    pages.append(pg(
        heading("1.4 Project Objectives"),
        table(["No.", "Objective"], [
            ["1", "Detect violence and weapon-related threats from camera streams using AI models."],
            ["2", "Support faster response and prevention of criminal actions in local and global contexts."],
            ["3", "Store incidents with timestamps, camera data, alert levels, confidence scores, snapshots, and clips."],
            ["4", "Provide a dashboard for reviewing incidents, cameras, evidence, and reports."],
            ["5", "Run the web stack through Docker to simplify setup and avoid manual dependency installation."],
        ]),
        caption("Table 1.1: Project objectives")
    ))
    pages.append(para_pack(
        "1.5 Methodology",
        "The methodology starts by reading frames from a camera source. The frames are sent to AI services that apply the violence model or weapon model. If a model detects a suspicious event above the configured threshold, the service creates evidence and sends an incident payload to the backend.",
        "The backend validates the payload, stores the incident in MySQL, links it to a camera record, and makes it visible in the dashboard. The operator can then inspect the incident details and review the stored media."
    ))
    pages.append(pg(
        heading("1.6 Time Plan"),
        table(["Phase", "Main Work"], [
            ["Planning", "Define project idea, scope, and documentation structure."],
            ["Research", "Study computer vision, violence detection, weapon detection, and dashboard systems."],
            ["Implementation", "Build Laravel backend, React dashboard, AI services, API integration, and Docker setup."],
            ["Testing", "Test detection flow, incident API, evidence storage, and dashboard review."],
            ["Documentation", "Write chapters, user manual, conclusion, future work, and references."],
        ]),
        caption("Table 1.2: Time plan")
    ))
    pages.append(para_pack(
        "1.7 Documentation Organization",
        "Chapter 2 presents background and related work. Chapter 3 explains the system architecture and methods. Chapter 4 describes implementation and experiment results. Chapter 5 explains how to run the application using Docker. Chapter 6 concludes the project and presents future work.",
        "The appendices include a user manual and source-code location summary so readers can connect the documentation with the real project files."
    ))

    # Chapter 2, pages 16-22
    pages.append(para_pack("Chapter 2: Literature Review", "This chapter reviews the concepts and related systems that support the project. It focuses on computer vision, surveillance monitoring, violence detection, weapon detection, and AI-assisted incident management.", "The goal of the review is to show why an integrated AI and dashboard solution is useful for reducing detection delay."))
    pages.append(para_pack("2.1 Computer Vision", "Computer vision is a field of artificial intelligence that enables software to interpret visual information. In this project, computer vision is used to process frames from camera streams and identify risk indicators.", "Computer vision systems can support detection, classification, localization, and tracking. These capabilities are important when video streams contain fast events that are hard to follow manually."))
    pages.append(para_pack("2.2 Surveillance Monitoring Systems", "Traditional surveillance systems mainly record footage or display live streams for human operators. They are useful for evidence collection, but they do not always support immediate response.", "AI-assisted monitoring adds an automated analysis layer. It can raise alerts when suspicious patterns appear, allowing the operator to focus attention on the most important feed."))
    pages.append(para_pack("2.3 Violence Detection Techniques", "Violence detection attempts to identify physical actions that may represent fighting, assault, or aggressive behavior. Because violence depends on motion and context, many approaches analyze multiple frames instead of a single image.", "The violence service in this project uses a Keras model and frame processing to classify activity as normal or violent. The output is transformed into an incident when the confidence passes the detection threshold."))
    pages.append(para_pack("2.4 Weapon Detection Techniques", "Weapon detection identifies dangerous objects such as guns or knives in frames. YOLO models are commonly used because they can detect and localize objects efficiently.", "The project uses a YOLO-based weapon detection service. When a weapon is detected with enough confidence, the service saves evidence and sends a critical incident to the backend."))
    pages.append(pg(
        heading("2.5 Comparison of Monitoring Approaches"),
        table(["Approach", "Advantages", "Limitations"], [
            ["Manual CCTV", "Human judgment and simple setup", "Missed events, fatigue, and poor scalability"],
            ["Recording-only CCTV", "Evidence after the event", "No early warning or live response support"],
            ["AI-assisted monitoring", "Continuous scanning, alerts, and evidence workflow", "Requires model tuning and responsible operation"],
        ]),
        caption("Table 2.1: Comparison of monitoring approaches")
    ))
    # Chapter 3, pages 23-30
    pages.append(para_pack("Chapter 3: System Architecture and Methods", "The system architecture is separated into camera sources, AI services, backend API, database, storage, and operator dashboard. Each module has a clear role in the full workflow.", "The web stack is run with Docker Compose so the backend, frontend, Nginx, and MySQL can start without manually installing dependencies on the host machine."))
    pages.append(pg(heading("3.1 High-Level Architecture"), image_paragraph(), caption("Figure 3.1: Main Docker-based system architecture")))
    pages.append(pg(
        heading("3.2 Main System Modules"),
        table(["Module", "Role"], [
            ["Camera Module", "Represents sources and stores camera identifiers and district data."],
            ["AI Services", "Analyze frames, detect events, save evidence, and post incident payloads."],
            ["Incident API", "Receives and validates incidents from AI services."],
            ["Dashboard", "Displays incidents, cameras, evidence, and reports."],
            ["Docker Runtime", "Runs MySQL, Laravel backend, Nginx, and Vite frontend containers."],
        ]),
        caption("Table 3.1: Main system modules")
    ))
    pages.append(para_pack("3.3 Backend Architecture", "The backend is built with Laravel. It contains web controllers, API controllers, models, routes, database migrations, and views. The main database models are Camera, Incident, and User.", "The backend receives incident data from the AI services through /api/incidents and stores the result in MySQL. It also serves dashboard pages through the Nginx container."))
    pages.append(para_pack("3.4 Frontend Architecture", "The frontend uses React and Vite. It provides dashboard components for incident rows, camera lists, stream controls, alert badges, evidence links, and reporting views.", "The frontend container runs the Vite development server on port 5173, while the main application is accessed through Nginx on port 8000."))
    pages.append(para_pack("3.5 AI Service Architecture", "The Python AI services use OpenCV for frame capture and streaming. The weapon service loads a YOLO model. The violence service loads a Keras model.", "Both services can save snapshots and clips, then send an incident payload to the Laravel API. The repository also includes docker/ai/Dockerfile for the Python environment."))
    pages.append(pg(
        heading("3.6 Docker Deployment Architecture"),
        table(["Container", "Purpose", "Port"], [
            ["violence-mysql", "MySQL database", "3306"],
            ["violence-backend", "Laravel PHP-FPM backend", "9000 internal"],
            ["violence-nginx", "Nginx web server for Laravel public folder", "8000"],
            ["violence-frontend", "Vite development server", "5173"],
        ]),
        caption("Table 3.2: Docker containers used by the project")
    ))
    # Chapter 4, pages 31-41
    pages.append(para_pack("Chapter 4: Experiment and Results", "This chapter explains the implementation environment, data preparation, model usage, API integration, and testing results. The purpose is to show how the system works as a complete pipeline.", "The implementation was designed around a Docker-based web stack so the main services can run consistently across development machines."))
    pages.append(para_pack("4.1 Dataset", "The violence model is intended to classify activity from video frames, while the weapon model is intended to detect visible weapons. The project expects trained model files to be placed under storage/app/models.", "The required paths are storage/app/models/weapon/weapon_detection_yolov11m.pt for the weapon model and storage/app/models/violence/cctvmodel_advanced.keras for the violence model."))
    pages.append(para_pack("4.2 Weapon Detection Model", "The weapon detection service uses a YOLO model. YOLO is suitable for near-real-time object detection because it predicts object locations and classes efficiently.", "When the best weapon confidence reaches the configured threshold, the service treats the event as a critical incident and saves supporting evidence."))
    pages.append(para_pack("4.3 Violence Detection Model", "The violence detection service uses a Keras model to classify activity. If the prediction indicates violence above the threshold, the event is recorded as a high-priority incident.", "The service also annotates the stream with labels and confidence values so the operator can understand the current model output."))
    pages.append(para_pack("4.4 Software Tools", "The project uses Laravel, React, Vite, MySQL, Docker, Nginx, Python, OpenCV, Keras, YOLO, and ffmpeg. Each tool supports a specific part of the workflow.", "Docker is especially important because it runs the web stack without requiring manual installation of PHP, Composer, Node, or MySQL on the host machine."))
    pages.append(pg(
        heading("4.5 API Integration"),
        table(["Endpoint", "Method", "Purpose"], [
            ["/api/incidents", "GET", "Return stored incidents with camera data."],
            ["/api/incidents", "POST", "Receive incidents from AI services."],
            ["AI service /status", "GET", "Return service and camera status."],
            ["AI service /stream", "GET", "Return MJPEG stream."],
            ["AI service /start and /stop", "POST", "Control detection mode."],
        ]),
        caption("Table 4.1: Important system endpoints")
    ))
    pages.append(para_pack("4.6 Evidence Storage", "Evidence clips and snapshots are saved under storage/app/public/incidents/videos and storage/app/public/incidents/snapshots. Laravel exposes these files through the public storage link.", "Saved incident URLs allow the dashboard to show snapshots and open video clips when the operator inspects an incident."))
    pages.append(para_pack("4.7 Experimental Setup", "The web application is started using docker compose up --build. This builds and starts MySQL, Laravel backend, Nginx, and the Vite frontend server.", "AI services can be run separately when camera access is needed, especially on Windows where Docker Desktop may not pass the laptop webcam reliably into Linux containers."))
    pages.append(para_pack("4.8 Evaluation Metrics", "The system can be evaluated using functional correctness, response time, detection confidence, evidence availability, and dashboard usability. These metrics show whether the system helps operators review incidents quickly.", "For model-specific evaluation, metrics such as accuracy, precision, recall, and false-positive rate can be added when a labeled test dataset is available."))
    pages.append(para_pack("4.9 Discussion", "The project demonstrates that AI services and a web dashboard can be connected into one monitoring workflow. Docker improves repeatability for the web stack and reduces setup problems.", "The main limitation is camera access for AI containers on some Windows environments. For this reason, the documentation recommends running the web stack with Docker and running AI services directly when local webcam access is required."))

    # Remaining pages
    pages.append(para_pack("Chapter 5: Run the Application", "This chapter explains the correct way to run the project based on the actual repository setup. The project uses Docker to avoid manually installing PHP, Composer, Node, and MySQL dependencies.", "The main application is served through Nginx on port 8000, while Vite runs on port 5173 for frontend development."))
    pages.append(pg(
        heading("5.1 Docker Run Steps"),
        numbered("Install Docker Desktop and start the Docker engine."),
        numbered("Open a terminal in the folder that contains docker-compose.yml."),
        numbered("Make sure the environment uses DB_HOST=mysql, DB_DATABASE=violence, DB_USERNAME=violence, and DB_PASSWORD=violence."),
        numbered("Run docker compose up --build."),
        numbered("Open http://127.0.0.1:8000/login in the browser."),
        numbered("If needed, run docker exec violence-backend php artisan migrate --seed."),
        numbered("If needed, run docker exec violence-backend php artisan storage:link."),
    ))
    pages.append(para_pack("5.2 Operator Workflow", "After login, the operator can use the dashboard to view incident statistics, recent priority incidents, alert mix, camera information, and evidence links.", "The operator can inspect an incident to see event type, confidence, violence score, weapon flag, camera, district, snapshot, clip, and metadata."))
    pages.append(para_pack("5.3 Running AI Services", "The repository includes docker/ai/Dockerfile for the Python AI environment. However, because Windows Docker Desktop may not pass the laptop webcam reliably, the AI services can be run directly on Windows when webcam access is required.", "The weapon service and violence service post incidents to http://127.0.0.1:8000/api/incidents so they can be reviewed inside the Laravel dashboard."))
    pages.append(para_pack("5.4 Testing the Full Flow", "A complete test starts the Docker web stack, starts one AI service, checks the /status endpoint, triggers or submits an incident, and opens the dashboard to confirm the incident appears.", "The evidence page and incident details page should show the saved snapshot or clip when evidence is available."))
    pages.append(para_pack("Chapter 6: Conclusion", "The AI Violence Detection System presents a practical solution for AI-assisted monitoring. It combines computer vision with a web dashboard to support earlier awareness of violence and weapon-related events.", "The project is relevant locally in Egypt and globally because public places everywhere can benefit from faster detection, organized evidence, and improved operator focus."))
    pages.append(para_pack("6.1 Future Work", "Future work includes combining the weapon and violence models into one camera pipeline, improving datasets, adding mobile notifications, adding role-based permissions, and deploying to edge devices.", "The system can also be extended with map-based incident visualization and more advanced reporting for security teams."))
    pages.append(pg(
        heading("References"),
        numbered('Laravel Documentation, "Laravel Web Framework Documentation", Laravel, 2026.'),
        numbered('React Documentation, "React User Interface Library Documentation", Meta, 2026.'),
        numbered('OpenCV Documentation, "Open Source Computer Vision Library", OpenCV, 2026.'),
        numbered('Ultralytics, "YOLO Object Detection Documentation", Ultralytics, 2026.'),
        numbered('TensorFlow/Keras Documentation, "Keras Deep Learning API", Google, 2026.'),
    ))
    pages.append(para_pack("Appendix A: User Manual", "Use Docker Compose to start the web stack. The important command is docker compose up --build. The application should be opened from http://127.0.0.1:8000/login.", "For AI testing, place model files in the configured storage paths, start one AI service, check the service status, and review incidents in the dashboard."))
    pages.append(para_pack("Appendix B: Main Source Code Locations", "Main Laravel controllers are located under app/Http/Controllers. Models are located under app/Models. API routes are located in routes/api.php and web routes are located in routes/web.php.", "AI services are located under ai_service. Docker configuration is located in docker-compose.yml and the docker folder. Frontend React components are located under resources/js/components."))

    assert len(pages) == 49, f"expected 49 pages, got {len(pages)}"
    body = "".join(pages)
    sect = (
        '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
        '<w:cols w:space="720"/><w:docGrid w:linePitch="360"/></w:sectPr>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas" '
        'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
        'xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        'xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
        'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
        'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" mc:Ignorable="w14 wp14"><w:body>'
        + body + sect + "</w:body></w:document>"
    )


def write_docx():
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
    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>"""
    doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/><Relationship Id="rIdNumbering" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/><Relationship Id="rIdImage1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/documentation_architecture.png"/></Relationships>"""
    core = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>AI Violence Detection System Documentation</dc:title><dc:creator>Codex</dc:creator></cp:coreProperties>"""
    app = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Microsoft Word</Application></Properties>"""
    if OUT.exists():
        OUT.unlink()
    with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/document.xml", document_xml_49())
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
