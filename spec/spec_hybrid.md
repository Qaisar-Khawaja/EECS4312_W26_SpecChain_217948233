# Requirement ID: FR_hybrid_1
- Description: [The system shall maintain active sleep-tracking sessions in the background with 99.9% persistence, preventing OS-level termination during low-memory states.]
- Source Persona: [PH1 (Stability-Driven Tracker)]
- Traceability: [Derived from review group H1]
- Acceptance Criteria: [If a sleep session is active and the app is moved to the background, the session must continue logging data for at least 8 hours without interruption.]
- Notes: [Rewritten to replace vague "tracking" with a measurable 99.9% persistence metric.]

# Requirement ID: FR_hybrid_2
- Description: [The system shall implement a local state-save every 60 seconds to ensure data recovery after an unexpected application crash.]
- Source Persona: [PH1 (Stability-Driven Tracker)]
- Traceability: [Derived from review group H1]
- Acceptance Criteria: [If the app crashes, upon restart, the system must restore the session with no more than 60 seconds of data loss.]
- Notes: [Added a specific time-based recovery constraint that was missing from the automated version.]

# Requirement ID: FR_hybrid_3
- Description: [The application shall utilize no more than 15% of total CPU resources on legacy devices (Android 10+ / iOS 14+) to prevent thermal throttling]
- Source Persona: [PH1 (Stability-Driven Tracker)]
Traceability: [Derived from review group H1]
Acceptance Criteria: [While tracking is active on a supported legacy device, the internal device temperature must not exceed 40°C.]
Notes: [Refined to include specific hardware versions and CPU limits for testability.]


# Requirement ID: FR_hybrid_4
Description: [The system shall provide a "Crash Report" diagnostic tool to send automated logs to technical support after a failed session.]
Source Persona: [PH1 (Stability-Driven Tracker)]
Traceability: [Derived from review group H1]
Acceptance Criteria: [If a crash is detected, the user must be presented with a one-tap option to transmit a diagnostic package to the support team.]
Notes: [Converted a vague "support" requirement into a functional diagnostic feature.]

# Requirement ID: FR_hybrid_5
Description: [The system shall provide a "One-Click Cancel" button within the main settings menu to allow for rapid subscription termination.]

Source Persona: [PH2 (Transparency-Focused Subscriber)]

Traceability: [Derived from review group H2]

Acceptance Criteria: [A user must be able to reach the cancellation confirmation screen in no more than two taps from the settings menu.]

Notes: [Rewritten to specifically target "dark patterns" identified in the hybrid review group.]

# Requirement ID: FR_hybrid_6
Description: [The system shall display clear "Premium" labeling and price disclosure on all locked content thumbnails.]

Source Persona: [PH2 (Transparency-Focused Subscriber)]

Traceability: [Derived from review group H2]

Acceptance Criteria: [If a content item requires a subscription, the exact price or subscription tier must be visible before the user clicks the item.]

Notes: [Improved from the automated version to require price transparency before the click-through.]

# Requirement ID: FR_hybrid_7
Description: [The system shall send an automated push notification and email 48 hours before a free trial converts to a paid subscription.]

Source Persona: [PH2 (Transparency-Focused Subscriber)]

Traceability: [Derived from review group H2]

Acceptance Criteria: [The system must log a sent-timestamp for both notification channels exactly 48 hours before the billing cycle begins.]

Notes: [Added multi-channel notification requirements to ensure user awareness.]

# Requirement ID: FR_hybrid_8
Description: [The system shall provide a "Billing History" tab where users can download PDF invoices for the last 24 months.]

Source Persona: [PH2 (Transparency-Focused Subscriber)]

Traceability: [Derived from review group H2]

Acceptance Criteria: [The user must be able to view and download a valid tax invoice for any transaction in their history.]

Notes: [Formalized the billing history requirement into a functional document-retrieval feature.]

# Requirement ID: FR_hybrid_9
Description: [The system shall enable an in-app dispute form that automatically attaches account and transaction metadata.]

Source Persona: [PH2 (Transparency-Focused Subscriber)]

Traceability: [Derived from review group H2]

Acceptance Criteria: [When a user submits a dispute, the form must automatically include the Transaction ID and User ID in the metadata.]

Notes: [Added automation to the support process to reduce user effort.]

# Requirement ID: FR_hybrid_10
Description: [The system shall allow for the download and offline playback of up to 500MB of audio content.]

Source Persona: [PH3 (Offline Relaxation Seeker)]

Traceability: [Derived from review group H3]

Acceptance Criteria: [Downloaded tracks must play in Airplane Mode without requiring a server-side license check for 30 days.]

Notes: [Specified the offline window and storage limits for better engineering constraints.]

# Requirement ID: FR_hybrid_11
Description: [The system shall provide an audio mixer to independently adjust the volume of guide voices versus background sounds.]

Source Persona: [PH3 (Offline Relaxation Seeker)]

Traceability: [Derived from review group H3]

Acceptance Criteria: [The user must be able to set the guide voice to 0% while background audio remains at 100%.]

Notes: [Improved testability by defining the specific behavior of the mixer.]

# Requirement ID: FR_hybrid_12
Description: [The system shall allow users to create and loop custom sleep playlists from their downloaded content.]

Source Persona: [PH3 (Offline Relaxation Seeker)]

Traceability: [Derived from review group H3]

Acceptance Criteria: [The system must support the continuous looping of at least three combined tracks without gap-related audio pops.]

Notes: [Added a technical quality requirement regarding "gapless" playback.]

# Requirement ID: FR_hybrid_13
Description: [The system shall sync sleep duration data to OS-level health APIs (HealthKit/Google Fit) within 10 seconds of session completion.]

Source Persona: [PH1, PH3]

Traceability: [Derived from review groups H1 and H3]

Acceptance Criteria: [Upon session end, the external health app must reflect the exact duration logged in the primary application.]

Notes: [Added a 10-second performance window for the data sync.]

# Requirement ID: FR_hybrid_14
Description: [The system shall provide a "Data Export" feature to download all historical sleep trends in CSV format.]

Source Persona: [PH1, PH3]

Traceability: [Derived from review groups H1 and H3]

Acceptance Criteria: [The exported CSV must contain Date, Start Time, End Time, and Quality Score columns.]

Notes: [Specified the exact data columns required for a valid export.]
