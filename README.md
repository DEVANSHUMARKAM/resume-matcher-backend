# Resume Matcher - Backend

A powerful backend application built with Spring Boot that provides intelligent resume matching capabilities using Natural Language Processing (NLP) and machine learning algorithms to compare resumes against job descriptions.

## 🚀 Features

- **Resume Parsing**: Automatically extract skills, experiences, and qualifications from uploaded resumes (PDF, DOCX formats)
- **Job Description Analysis**: Parse and extract key requirements, skills, and keywords from job descriptions
- **Intelligent Matching Algorithm**: Calculate similarity scores between resumes and job descriptions using NLP techniques
- **RESTful API**: Well-structured REST endpoints for seamless integration with frontend applications
- **Multi-format Support**: Handle various resume formats and extract meaningful information
- **ATS Compatibility Check**: Evaluate resumes against Applicant Tracking System standards
- **Keyword Extraction**: Identify matching and missing keywords between resume and job description

## 🛠️ Tech Stack

- **Java** - Primary programming language
- **Spring Boot** - Application framework
- **Spring Web** - RESTful web services
- **Spring Data JPA** - Database persistence
- **MySQL/PostgreSQL** - Relational database
- **Apache PDFBox** - PDF processing
- **Apache POI** - Document processing (DOCX)
- **Apache OpenNLP** - Natural Language Processing
- **Maven** - Dependency management and build tool

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

- Java 17 or higher
- Maven 3.6+
- MySQL 8.0+ or PostgreSQL 12+
- Git

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/DEVANSHUMARKAM/resume-matcher-backend.git
cd resume-matcher-backend
```

### 2. Configure Database

Create a database for the application:

```sql
CREATE DATABASE resume_matcher;
```

Update `src/main/resources/application.properties` with your database credentials:

```properties
# Database Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/resume_matcher
spring.datasource.username=your_username
spring.datasource.password=your_password
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true

# File Upload Configuration
spring.servlet.multipart.max-file-size=10MB
spring.servlet.multipart.max-request-size=10MB

# Server Configuration
server.port=8080
```

### 3. Build the project

```bash
mvn clean install
```

### 4. Run the application

```bash
mvn spring-boot:run
```

The server will start at `http://localhost:8080`

## 🔌 API Endpoints

### Resume Matching

```http
POST /api/match
Content-Type: multipart/form-data

Parameters:
- resume: MultipartFile (PDF/DOCX)
- jobDescription: String

Response:
{
  "matchPercentage": 75.5,
  "matchingKeywords": ["Java", "Spring Boot", "REST API"],
  "missingKeywords": ["Docker", "Kubernetes"],
  "recommendations": ["Add Docker experience", "Highlight cloud skills"],
  "atsScore": 82.0
}
```

### Upload Resume

```http
POST /api/resume/upload
Content-Type: multipart/form-data

Parameters:
- file: MultipartFile

Response:
{
  "id": 1,
  "fileName": "resume.pdf",
  "extractedText": "...",
  "skills": ["Java", "Spring Boot"],
  "uploadDate": "2025-11-13T19:03:00"
}
```

### Analyze Job Description

```http
POST /api/job-description/analyze
Content-Type: application/json

Body:
{
  "description": "We are looking for a Java developer..."
}

Response:
{
  "requiredSkills": ["Java", "Spring Boot", "MySQL"],
  "experienceLevel": "Mid-level",
  "keywords": ["backend", "API", "database"],
  "educationRequirements": "Bachelor's in Computer Science"
}
```

### Get Resume Details

```http
GET /api/resume/{id}

Response:
{
  "id": 1,
  "fileName": "resume.pdf",
  "skills": ["Java", "Spring Boot"],
  "experience": ["Software Developer at XYZ"],
  "education": ["B.Tech in Computer Science"]
}
```

## 📁 Project Structure

```
resume-matcher-backend/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── resumematcher/
│   │   │           ├── controller/      # REST controllers
│   │   │           ├── service/         # Business logic
│   │   │           ├── repository/      # Data access layer
│   │   │           ├── model/           # Entity classes
│   │   │           ├── dto/             # Data transfer objects
│   │   │           ├── util/            # Utility classes
│   │   │           └── config/          # Configuration classes
│   │   └── resources/
│   │       ├── application.properties   # Configuration file
│   │       └── static/                  # Static resources
│   └── test/                            # Unit and integration tests
├── pom.xml                              # Maven configuration
└── README.md
```

## 🧪 Testing

Run the tests using Maven:

```bash
mvn test
```

## 🔐 Security Considerations

- Implement file type validation for uploads
- Add file size limits to prevent DoS attacks
- Sanitize user inputs to prevent injection attacks
- Use HTTPS in production
- Implement authentication and authorization (JWT recommended)

## 🚀 Deployment

### Using JAR

```bash
mvn clean package
java -jar target/resume-matcher-backend-0.0.1-SNAPSHOT.jar
```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Build and run:

```bash
docker build -t resume-matcher-backend .
docker run -p 8080:8080 resume-matcher-backend
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Environment Variables

For production deployment, use environment variables:

```bash
export DB_URL=jdbc:mysql://localhost:3306/resume_matcher
export DB_USERNAME=your_username
export DB_PASSWORD=your_password
export SERVER_PORT=8080
```

## 🐛 Known Issues

- Large PDF files (>10MB) may take longer to process
- OCR functionality for scanned PDFs not yet implemented

## 📚 Future Enhancements

- [ ] Support for more file formats (RTF, TXT)
- [ ] OCR for scanned resume documents
- [ ] Advanced ML models for better matching accuracy
- [ ] Batch processing for multiple resumes
- [ ] Redis caching for improved performance
- [ ] Elasticsearch integration for better search capabilities
- [ ] Email notification service
- [ ] Resume template suggestions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Devanshu Markam**

- GitHub: [@DEVANSHUMARKAM](https://github.com/DEVANSHUMARKAM)

## 🙏 Acknowledgments

- Apache OpenNLP for NLP capabilities
- Spring Boot community for excellent documentation
- All contributors who help improve this project

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub or contact the maintainer.

---

**Note**: Make sure to update the frontend application URL in CORS configuration before deploying to production.
