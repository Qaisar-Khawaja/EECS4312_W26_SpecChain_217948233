# Requirement ID: FR1
- Description: [The system shall provide a "Restore Purchase" button in the account settings to manually re-verify subscription status with the with the Google Play Store or Apple App Store, with the verification completing within 5 seconds under normal network conditions.]
- Source Persona: [ Locked-Out Linda (P1)]
- Traceability: [Derived from review group G1]
- Acceptance Criteria: [ Given a user with an active subscription but "Free" status, when they navigate to settings > accounts and click "Restore Purchase", then the system shall validate the receipt with the store API within 5 seconds and upgrade the account status to Premium without requiring logout or app restart and a success message "Subscription restored successfully" shall be displayed and premium content shall be immediately accessible]

# Requirement ID: FR2
- Description: [ The application shall implement a "Remember Me" token system that preserves user login state across app updates, using refresh tokens with a 90-day expiration period.]
- Source Persona: [Locked-Out Linda (P1) ]
- Traceability: [Derived from review group G1 ]
- Acceptance Criteria: [ Given a logged-in user, when the app is updated to a newer version, then the user must remain authenticated upon the first launch after the update.]

# Requirement ID: FR3
- Description: [The system shall display a distinct "Premium" visual badge on all meditation tiles that are not accessible to free-tier users. ]
- Source Persona: [Budget-Conscious Ben (P2) ]
- Traceability: [ Derived from review group G2]
- Acceptance Criteria: [Given a user on the free tier, when they browse the "Explore" library, then every subscription-only session must show a lock icon before the user clicks on it.]

# Requirement ID: FR4
- Description: [The system shall provide a "Free Sessions" filter in the search results.]
- Source Persona: [Budget-Conscious Ben (P2) ]
- Traceability: [Derived from review group G2 ]
- Acceptance Criteria: [Given a user searching for content, when they apply the "Free" filter, then only non-subscription-gated sessions must be displayed in the results. ]

# Requirement ID: FR5
- Description: [The application shall utilize a high-priority background service and Android "WakeLock" to prevent audio sessions from being killed by OS battery optimization. ]
- Source Persona: [ Sleepless Sarah (P3)]
- Traceability: [Derived from review group G3 ]
- Acceptance Criteria: [Given a long-form Sleepcast is playing, when the phone screen is locked and the device enters "Doze" mode, then the audio must continue playing without interruption. ]

# Requirement ID: FR6
- Description: [The system shall allow playback of fully downloaded content without requiring an initial "heartbeat" check with the server. ]
- Source Persona: [ Sleepless Sarah (P3)]
- Traceability: [Derived from review group G3 ]
- Acceptance Criteria: [Given the device is in Airplane Mode, when the user selects a session from their "Downloads" folder, then the audio must begin playing immediately. ]

# Requirement ID: FR7
- Description: [The system shall provide a "Minimalist Home" toggle in the settings that hides promotional banners and social "community" features. ]
- Source Persona: [Minimalist Mark (P4) ]
- Traceability: [ Derived from review group G4]
- Acceptance Criteria: [ Given the "Minimalist Home" is enabled, when the user views the home screen, then only the search bar and the user's current course should be visible.]

# Requirement ID: FR8
- Description: [The navigation architecture shall limit core feature access (Breathing, Meditating, Sleeping) to no more than two clicks from the launch screen.]
- Source Persona: [ Minimalist Mark (P4)]
- Traceability: [Derived from review group G4 ]
- Acceptance Criteria: [Given the user is on the home screen, when they want to start a "Basic Breathing" exercise, then they must be able to reach the player interface in two taps or fewer. ]

# Requirement ID: FR9
- Description: [ The system shall implement a local database to store "Meditation Streaks" that syncs in the background to prevent data loss during server outages.]
- Source Persona: [ Zen Zoe (P5)]
- Traceability: [Derived from review group G5 ]
- Acceptance Criteria: [Given the user completes a session while offline, when the device reconnects to the internet, then the local streak count must merge correctly with the server-side count without resetting. ]

# Requirement ID: FR10
- Description: [ The application shall provide a "Legacy Voice" option for core meditation courses even when the content library is refreshed with new recordings.]
- Source Persona: [Zen Zoe (P5) ]
- Traceability: [ Derived from review group G5]
- Acceptance Criteria: [ Given a core course is updated with a new narrator, when the user opens the course settings, then they must have the option to toggle back to the previous narrator's audio files.]

# Requirement ID: FR11
- Description: [The system shall provide an automated "Emergency Offline Mode" that triggers when a server-side 5xx error is detected, allowing users to access their last 3 played sessions. ]
- Source Persona: [ Zen Zoe (P5)]
- Traceability: [Derived from review group G5 (Positive Impact / Dependency) ]
- Acceptance Criteria: [Given the Headspace servers are down, when the user opens the app, then the app must not hang on a loading screen and instead must display the "Recent Offline Sessions" menu. ]

# Requirement ID: FR12
- Description: [The application shall provide a "Dark Mode" UI setting that follows the system-wide Android/iOS theme to reduce blue-light exposure for late-night users. ]
- Source Persona: [ Sleepless Sarah (P3)]
- Traceability: [Derived from review group G3 (Nighttime Audio) ]
- Acceptance Criteria: [ Given the device is in System Dark Mode, when the app is launched, then all backgrounds must be #000000 or dark grey to prevent eye strain in a dark room.]

# Requirement ID: FR13
- Description: [The system shall implement an "Activity Log Verification" tool that allows users to manually re-add a meditation session to their history if the app crashed during the session. ]
- Source Persona: [ Zen Zoe (P5)]
- Traceability: [Derived from review group G5 (Streak Maintenance) ]
- Acceptance Criteria: [Given a session was interrupted by an app crash, when the user re-opens the app, then a prompt must appear asking if they would like to "Mark Session as Complete" to save their streak. ]

# Requirement ID: FR14
- Description: [The app shall display the total file size of a meditation course and the remaining device storage space before a user initiates a download. ]
- Source Persona: [Budget-Conscious Ben (P2) / Minimalist Mark (P4) ]
- Traceability: [Derived from review group G2 and G4 (Resource Management) ]
- Acceptance Criteria: [ Given a user clicks "Download" on a course, when the confirmation pop-up appears, then it must state the exact MB size and verify if the device has sufficient space.]
