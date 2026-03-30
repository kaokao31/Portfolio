# 📡 Computer Network — Course Portfolio

> **นายกานดิทัต นามสุดตา**  
> สาขาวิชา Computer Science | มหาวิทยาลัยขอนแก่น (Khon Kaen University)  
> 📧 [kanditat.n@kkumail.com](mailto:kanditat.n@kkumail.com)

---

## 📖 เกี่ยวกับ Repository นี้

Repository นี้เป็นที่รวบรวมไฟล์งานทั้งหมดของวิชา **Computer Network** ประกอบด้วย Lab, Assignment และ Project ที่ได้ทำตลอดภาคการศึกษา ครอบคลุมเนื้อหาตั้งแต่พื้นฐานการสื่อสารเครือข่าย ไปจนถึงการออกแบบและพัฒนาระบบเครือข่ายขั้นสูง

---

## 📂 โครงสร้างไฟล์

```
📦 Computer-Network-Portfolio
├── 📁 Lab/
│   ├── Lab_01 — Protocol & OSI Layer Analysis (ARP, ICMP, Ethernet)
│   ├── Lab_02 — VLAN Configuration & Router-on-a-Stick
│   ├── Lab_03 — MIME File Transfer over Inter-VLAN Network
│   ├── Lab_04 — Simulated Internet with NAT, Static Routing & Stateful/Stateless Services
│   └── Lab_05 — Internet Edge Router, WAN Serial Link & NAT
│
├── 📁 Assignments/
│   ├── Assignment_01 — Computer Networks in Daily Life (Essay)
│   ├── Assignment_02 — Network Topology Analysis (Point-to-Point, LAN, Router)
│   └── Assignment_03 — Packet Tracer Network Design
│
└── 📁 Project/
    └── AetherWeave 2.0 — Adaptive Overlay Network
```

---

## 🧪 Labs

### Lab 1 — Protocol Header & OSI Layer Analysis
ศึกษาการทำงานของโปรโตคอล ARP, ICMP และ Ethernet ผ่าน Cisco Packet Tracer  
วิเคราะห์ Protocol Header ในแต่ละชั้น OSI และทดสอบ Connectivity ระหว่าง PC1 และ PC2  
รวมถึงการ Troubleshoot ปัญหา Wrong Subnet Mask, Interface Shutdown และ Incorrect Gateway

### Lab 2 — VLAN Configuration & Router-on-a-Stick
ตั้งค่า VLAN บน Cisco Switch (VLAN 10: USERS, VLAN 20: SERVERS, VLAN 99: MANAGEMENT, VLAN 999: BLACKHOLE)  
กำหนด Trunk Port, Access Port และตั้งค่า Router Subinterface เพื่อทำ Inter-VLAN Routing  
ทดสอบ Connectivity แบบ End-to-End ระหว่างอุปกรณ์ใน VLAN ที่แตกต่างกัน

### Lab 3 — MIME File Transfer over Inter-VLAN Network
ออกแบบระบบ MIME-based File Transfer ระหว่าง Client (VLAN 10) และ Server (VLAN 20)  
ศึกษาการทำงาน TCP Three-Way Handshake, ARP Resolution และการ Capture Packet ผ่าน Wireshark  
วิเคราะห์ Encapsulation Chain ตั้งแต่ Application Layer จนถึง Physical Layer

### Lab 4 — Simulated Internet with NAT & Stateless/Stateful Services
จำลองอินเทอร์เน็ต (10.10.12.0/30) เชื่อม 2 Private LAN ผ่าน Router R1 และ R2  
ตั้งค่า Static Routing, NAT Overload และ Deploy Mockup Infrastructure  
เปรียบเทียบพฤติกรรมของ Stateless API (Port 3000) และ Stateful API (Port 3001) ทั้งใน Local และ Remote Network

### Lab 5 — Internet Edge Router & WAN Serial Link
ออกแบบระบบเครือข่ายแบบ Internet Edge โดยใช้ Serial WAN (100.10.10.0/30) เชื่อม R1 และ R2  
ตั้งค่า Static Routing, NAT PAT (Overload) และทดสอบ Connectivity ข้ามเครือข่าย (LAN A → LAN B)

---

## 📝 Assignments

### Assignment 1 — Computer Networks in Daily Life
เรียงความบรรยายถึงบทบาทของ Computer Network ในชีวิตประจำวัน  
ครอบคลุมการใช้งาน Social Media, Google Maps, Mobile Banking และ Email ผ่าน Wi-Fi และ Mobile Network

### Assignment 2 — Network Topology Analysis
วิเคราะห์โครงสร้างเครือข่าย 3 รูปแบบจากภาพ Cisco Packet Tracer ได้แก่:
- **กลุ่มที่ 1** — Point-to-Point Network (PC0 ↔ PC1)
- **กลุ่มที่ 2** — LAN Network with Switch (PC2, PC3, PC4 ผ่าน Switch0)
- **กลุ่มที่ 3** — LAN Network with Router (2 LAN เชื่อมกันด้วย ISR4321)

### Assignment 3 — Packet Tracer Network Design
ไฟล์ `.pkt` สำหรับการออกแบบเครือข่ายใน Cisco Packet Tracer

---

## 🚀 Project — AetherWeave 2.0: Adaptive Overlay Network

> ระบบ Adaptive Overlay Network ที่เปลี่ยนเครือข่ายแบบเดิมสู่การคาดการณ์และปรับตัวได้เอง  
> ผ่านอัลกอริทึมการเลือกเส้นทางอัจฉริยะและการรักษาความปลอดภัยในระดับโครงสร้าง

### ✨ Features หลัก
- **Adaptive Routing** — เลือกเส้นทางที่มีประสิทธิภาพสูงสุดด้วย Dijkstra's Algorithm แบบ Real-time
- **Self-Healing** — ระบบกู้คืนอัตโนมัติภายใน 5 วินาทีเมื่อ Node ล่ม
- **Packet Validation** — ตรวจสอบความถูกต้องของข้อมูลด้วย AES-256, RSA และ Packet Signature
- **99%+ Delivery Rate** — อัตราการส่ง Packet สำเร็จมากกว่า 99%
- **20-25% Lower Latency** — ลด Latency เทียบกับเส้นทางปกติ

### 🏗️ สถาปัตยกรรม (6-Layer Architecture)
```
┌─────────────────────┐
│    Overlay Node     │
├─────────────────────┤
│   Routing Engine    │
├─────────────────────┤
│      Security       │
├─────────────────────┤
│     Monitoring      │
└─────────────────────┘
```

### 📊 ผลการทดสอบ KPI

| ตัวชี้วัด (KPI)              | เป้าหมาย   | ผลการทดสอบจริง          |
|-----------------------------|------------|------------------------|
| Recovery Time               | ≤ 5 วินาที | ✅ กู้คืนทันทีหลัง Node ล่ม |
| Packet Validation           | ≥ 99%      | ✅ ส่งสำเร็จทุก Packet    |
| Test Coverage               | ≥ 80%      | ✅ ครอบคลุมทุกส่วนประกอบ  |

### ▶️ วิธีรัน Demo

```bash
# ติดตั้ง dependencies
pip install networkx matplotlib

# รัน Demo
python aetherweave_demo.py
```

### 👥 สมาชิกกลุ่ม Project

| รหัสนักศึกษา  | ชื่อ                        | Role               |
|--------------|-----------------------------|--------------------|
| 673380392-1  | นายกานดิทัต นามสุดตา        | Network Architects |
| 673380395-5  | นายคมชาญ น้อยเนียม          | IaC/DevOps         |
| 673380420-2  | นายภีมเดช กลั่นกิ่ง         | QA/Test            |
| 673380408-2  | นายธีธัช ลิ้มประยูรวงศ์     | IaC/DevOps         |
| 673380430-9  | นายอนันต์เอกก์ใหญ่พงศกร    | Network Architects |
| 673380589-2  | นายปฏิภาณ มะนิลทิพย์       | IaC/DevOps         |

---

## 🛠️ Tools & Technologies

![Cisco Packet Tracer](https://img.shields.io/badge/Cisco_Packet_Tracer-1BA0D7?style=flat&logo=cisco&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![NetworkX](https://img.shields.io/badge/NetworkX-013243?style=flat)
![Wireshark](https://img.shields.io/badge/Wireshark-1679A7?style=flat&logo=wireshark&logoColor=white)

---

## 📬 ติดต่อ

**นายกานดิทัต นามสุดตา**  
📧 [kanditat.n@kkumail.com](mailto:kanditat.n@kkumail.com)  
🏫 สาขาวิชา Computer Science | คณะวิทยาศาสตร์ | มหาวิทยาลัยขอนแก่น
