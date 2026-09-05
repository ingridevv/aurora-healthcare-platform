# Discovery Workshop #1 – Current Data Landscape


---

## Objective

Understand the current healthcare ecosystem, existing systems, integration patterns, business processes and pain points before defining the platform architecture.

---

## Discussion

### Current Systems Landscape

**Consultant**

Can you describe the systems currently operating across the organization?

**Client**

Different hospitals have acquired systems independently over the years.

Our largest hospital uses **Epic** as the Electronic Health Record (EHR).

Laboratories operate a separate **Laboratory Information System (LIS)** from another vendor.

Radiology uses its own PACS/RIS platform.

Financial operations and claims are managed inside SAP ERP.

Some outpatient clinics still export flat files every night.

---

### Integration Strategy

**Consultant**

How do these systems exchange information today?

**Client**

There isn't a single integration strategy.

Some insurance companies expose secure REST APIs.

Smaller providers still exchange files using SFTP.

Several internal clinics still generate CSV exports during nightly batches.

Laboratory results are synchronized back to Epic every few minutes.

---

### Operational Architecture

**Consultant**

Are these systems fully integrated?

**Client**

Not completely.

Each operational system owns part of the patient journey.

Information moves between systems, but not always immediately.

---

### Master Data

**Consultant**

How do different systems identify the same patient?

**Client**

Each platform maintains its own identifier.

Epic generates its own Patient ID.

Laboratory systems use another identifier.

Billing references financial customer numbers.

There is no enterprise-wide master patient identifier.

Analysts manually reconcile patients during reporting.

---

### Clinical Operations

**Consultant**

How are laboratory and imaging results made available?

**Client**

Laboratory instruments send results to the LIS.

The laboratory validates them before publishing.

Critical values are propagated immediately.

Routine laboratory exams synchronize every few minutes.

Radiology follows a similar process.

---

### Claims Processing

**Consultant**

How does insurance approval work?

**Client**

Claims are processed inside SAP.

Some providers answer almost immediately through APIs.

Others respond only after scheduled batch exchanges.

---

## Observations

During the discussion several architectural observations emerged.

* Operational data is fragmented across multiple business systems.
* Different departments own different portions of the patient lifecycle.
* Multiple integration mechanisms coexist (REST APIs, SFTP and batch files).
* Synchronization latency varies depending on the business process.
* Patient identity reconciliation is currently a manual activity.
* Laboratory information follows an event-driven workflow after validation.
* Historical data exists across several isolated platforms.

---

## Initial Risks Identified

| Risk                             | Impact                           |
| -------------------------------- | -------------------------------- |
| No enterprise patient identifier | Difficult patient reconciliation |
| Fragmented operational systems   | No unified patient view          |
| Mixed integration patterns       | Higher operational complexity    |
| Delayed synchronization          | Clinical inconsistency risks     |
| Manual reconciliation            | Reduced operational efficiency   |

---

## Follow-up Questions

* Is there an initiative to implement a Master Patient Index (MPI)?
* Which datasets contain HIPAA Protected Health Information?
* Which integrations require real-time processing?
* Which systems are considered authoritative for patient data?
* What are the expected SLAs for each critical business event?
