#  Smart Factory Orchestration Platform

A simulation-based, cloud-native smart factory orchestration system built using FastAPI, MQTT, Celery, Redis, and MongoDB. This system supports role-based control, real-time data streams, background processing, and predictive maintenance to serve as a foundation for Industry 4.0 solutions.

---

##  Project Summary

This platform simulates a real-time, secure, and intelligent factory monitoring system. It supports interaction between users and machine simulators via MQTT and provides REST and WebSocket interfaces for monitoring, control, and reporting.

---

##  Features

-  **Real-Time Production Monitoring**
-  **Predictive Maintenance Scheduling**
-  **Downtime Detection and Alerting**
-  **Role-Based Access Control (RBAC)**
-  **Detailed Reporting APIs**
-  **WebSocket Dashboard for Live Updates**
-  **Comprehensive Event Logging (MongoDB)**
-  **Machine Simulator Script for Testing**

---

##  Tech Stack

| Component       | Technology            |
|----------------|------------------------|
| API & UI       | FastAPI, WebSocket     |
| Messaging      | MQTT (EMQX Broker)     |
| Background Tasks | Celery + Redis        |
| Database       | MongoDB                |
| Security       | JWT, RBAC, Rate Limiting |


---

##  Architecture Flow

1. **User** logs in via FastAPI → receives JWT
2. **JWT** contains role & permissions → passed to API
3. **FastAPI Server** validates and routes:
   - Sends tasks to **Redis**
   - Streams updates via **WebSocket**
4. **Celery Workers** process tasks:
   - Calculate efficiency
   - Schedule maintenance
   - Publish to **EMQX MQTT Broker**
5. **MongoDB** logs all events & command metadata
6. **Simulated Machines**:
   - Send metrics via MQTT
   - Receive control commands

![Vertical Flowchart](./A_flowchart_diagram_illustrates_an_architecture_fo.png)

---

## 🔐 Authentication & Roles

- JWT-based authentication
- RBAC enforced at route level
- Roles:
  - **Admin**: Full access
  - **Engineer**: Limited to assigned lines
  - **Operator**: View-only for assigned machines

---

##  MongoDB Schema

| Collection         | Purpose                              |
|--------------------|--------------------------------------|
| `machines`         | Registered machine info              |
| `events`           | All MQTT messages                    |
| `maintenance`      | Scheduled/completed tasks            |
| `downtime_alerts`  | Inactivity alerts                    |
| `users`            | User roles, hashed credentials       |


---

## 
