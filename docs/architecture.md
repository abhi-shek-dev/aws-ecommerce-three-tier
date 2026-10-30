# AWS Three-Tier Highly Available E-Commerce Platform

## Architecture Overview

This project implements a production-style, highly available three-tier e-commerce application on AWS.

The infrastructure is deployed across multiple Availability Zones to eliminate single points of failure and provide scalability, security, and fault tolerance.

---

## High-Level Architecture

Internet Users
      │
      ▼
CloudFront Distribution
      │
      ▼
Internet-Facing Application Load Balancer (External ALB)
      │
      ▼
Auto Scaling Group - Web Tier (Nginx)
      │
      ▼
Internal Application Load Balancer
      │
      ▼
Auto Scaling Group - Application Tier (Flask)
      │
      ▼
Amazon RDS MySQL (Multi-AZ)
      │
      ▼
Persistent Application Data

---

## Network Architecture

AWS Region
│
└── VPC (10.0.0.0/16)
    │
    ├── Availability Zone A
    │   │
    │   ├── Public Subnet A
    │   │   ├── NAT Gateway A
    │   │   ├── External ALB
    │   │   └── Bastion Host
    │   │
    │   ├── Private Web Subnet A
    │   │   └── Nginx Web Server
    │   │
    │   ├── Private App Subnet A
    │   │   └── Flask App Server
    │   │
    │   └── Private DB Subnet A
    │       └── RDS MySQL Primary
    │
    └── Availability Zone B
        │
        ├── Public Subnet B
        │   ├── NAT Gateway B
        │   │
        │   └── External ALB
        │
        ├── Private Web Subnet B
        │   └── Nginx Web Server
        │
        ├── Private App Subnet B
        │   └── Flask App Server
        │
        └── Private DB Subnet B
            └── RDS MySQL Standby

---

## AWS Services Used

### Networking
- Amazon VPC
- Internet Gateway
- NAT Gateway
- Route Tables
- Network Segmentation

### Compute
- Amazon EC2
- Launch Templates
- Auto Scaling Groups

### Load Balancing
- External Application Load Balancer
- Internal Application Load Balancer

### Security
- IAM Roles
- Security Groups
- Least Privilege Access Model

### Database
- Amazon RDS MySQL
- Multi-AZ Deployment

### Content Delivery
- Amazon CloudFront

### Monitoring
- Amazon CloudWatch
- CloudWatch Logs

### Source Control
- Git
- GitHub

---

## Security Design

### Public Access

Internet
    ↓
CloudFront
    ↓
External ALB

Only CloudFront and the External ALB are publicly accessible.

### Application Isolation

External ALB
    ↓
Web Tier

Web Tier
    ↓
Internal ALB

Internal ALB
    ↓
Application Tier

Application servers are deployed in private subnets and cannot be accessed directly from the internet.

### Database Protection

Application Tier
    ↓
RDS MySQL

Database servers reside in private database subnets and accept traffic only from application servers.

---

## IAM Roles

### EC2-WebServer-Role

Permissions:
- CloudWatch Logs
- SSM Session Manager
- Read-only access to application assets

### EC2-AppServer-Role

Permissions:
- RDS connectivity
- CloudWatch Logs
- Secrets Manager access

### CloudFront

Permissions:
- Access to application content origins

---

## High Availability Features

- Multi-AZ deployment
- Auto Scaling Groups
- Multiple application servers
- Multiple web servers
- Application Load Balancers
- RDS Multi-AZ failover
- CloudFront global edge locations

---

## Scaling Strategy

### Web Tier

Auto Scaling Policy:
- Scale Out: CPU > 70%
- Scale In: CPU < 30%

### Application Tier

Auto Scaling Policy:
- Scale Out: Request count increases
- Scale In: Low utilization

---

## Application Flow

User Request
    ↓
CloudFront
    ↓
External ALB
    ↓
Nginx Web Server
    ↓
Internal ALB
    ↓
Flask API Server
    ↓
RDS MySQL
    ↓
Response Returned To User

---

## How the application maps onto the tiers

| Tier | Runs | Notes |
|---|---|---|
| Web | Nginx on EC2 (Auto Scaling Group) | Serves `frontend/` and forwards `/api/*` to the internal ALB (`deploy/nginx.conf`) |
| App | Flask under gunicorn on EC2 (Auto Scaling Group) | `deploy/ecommerce-backend.service`; ALB health check path `/health` |
| Data | RDS MySQL | Schema in `database/schema.sql`; credentials from Secrets Manager (`DB_SECRET_ARN`) |

The browser calls relative `/api/...` URLs, so CloudFront, the external ALB and Nginx handle everything on one origin and the API is never reachable from the internet directly.

---

## Project Repository Structure

```
frontend/    static site
backend/     Flask API
database/    schema and sample data
deploy/      Nginx config, systemd unit, env template
docs/        this document
README.md
.gitignore
```
