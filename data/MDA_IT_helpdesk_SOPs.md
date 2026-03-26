### MDA IT Helpdesk - Standard Operating Procedures (SOPs)

#### 1. Updating HP USB-C Dock G5 Firmware
**Intent:** Use this when a user needs to update the firmware on their docking station.
* Go to the computer's web browser and navigate to the official HP Support website.
* Search for the specific "HP USB-C Dock G5" model to find the dedicated support page.
* On the support page, locate the "Software and Drivers" section, find the firmware update file, and download it.
* Once downloaded, run the installer file to begin the installation. A screen will indicate if the firmware is "Out of date".
* The installer will first "stage" the firmware; keep the computer connected during this phase.
* The power light on the dock will blink to indicate the update is being applied (typically takes a few minutes), and the dock will be unusable during this time.
* Once the power light stops blinking, the firmware update is complete.

#### 2. Troubleshooting Microsoft Teams Audio and Video
**Intent:** Use this when a user cannot hear, be heard, or be seen on a Microsoft Teams call.
* **Step 1: Check Connections.** Ensure the headset, webcam, or external mic/speakers are properly plugged in. If using Bluetooth, ensure the device is paired and connected.
* **Step 2: Verify Teams Settings.** In Teams, click the three dots next to the profile picture, go to Settings, then Devices. Select the correct Speaker, Microphone, and Camera, then use the "Make a test call" feature to verify.
* **Step 3: Check Windows Settings.** Right-click the sound icon in the taskbar, select Sound settings, and ensure the correct devices are selected and not muted. Go to Settings > Privacy > Camera to ensure camera access is enabled for Teams.
* **Step 4: Check System Permissions.** On Windows, go to Settings > Privacy & Security, and ensure Microphone and Camera access is enabled for Teams. On Mac, go to System Settings > Privacy & Security, and ensure Microsoft Teams is allowed under Microphone, Camera, and Accessibility.
* **Step 5: Restart Teams.** Fully quit Teams by right-clicking it in the system tray and selecting Quit, then restart the app.

#### 3. Connecting to MDA Wireless Networks (Wi-Fi)
**Intent:** Use this when a user needs the guest wifi password or needs to connect a device to the employee network.
* **MDA Guest Network (Requires Password Only):**
    * **Laptop:** Click the Wi-Fi icon, select "MDA Guest", enter the password `MDAWoolfolk!`, and click Connect.
    * **Mobile (iPhone/iPad):** Go to Settings > Wi-Fi, tap "MDA Guest", enter the password `MDAWoolfolk!`, and tap Join.
* **MDA Employee Network (Requires Personal Network Credentials):**
    * **Laptop:** Click the Wi-Fi icon, select "MDA Employee", enter the user's network username and password, accept any security certificates if prompted, and click Connect.
    * **Mobile (iPhone/iPad):** Go to Settings > Wi-Fi, tap "MDA Employee", enter network credentials, tap Join, and accept the certificate if prompted.

#### 4. Resetting Windows Computer Passwords
**Intent:** Use this when a user wants to change their standard computer login password.
* Press Ctrl + Alt + Delete on the keyboard.
* Select "Change a password".
* Enter the old password, then enter and confirm the new password.
* Press OK or Enter to finalize.
* **Password Requirements:** Must be 8-12 characters minimum; include uppercase, lowercase, numbers, and symbols; cannot be easily guessable (e.g., "123456" or "Password1"); and must not have been used recently.

#### 5. Restoring ScanSnap Scanner Connections
**Intent:** Use this when a user's ScanSnap scanner is not connecting to their computer.
* **Step 1: Restart Scanner.** Unplug the power from the scanner, wait at least ten seconds, and plug it back in.
* **Step 2: Restart Computer.** Reboot the computer.
* **Step 3: Power Cycle.** Unplug the USB cable from the computer or scanner, wait a few seconds, and reconnect it.
* **Step 4: Check Hardware.** Try a different USB cable and port.
* **Admin Escalation:** If standard steps fail, administrative privileges are required to reinstall the software or use the ScanSnap Recovery Tool located in the ScanSnap Manager/Home settings.

#### 6. Exiting Proofpoint Browser Isolation
**Intent:** Use this when a user complains a safe website is blocked, isolated, or they cannot download/upload files on a specific site.
* Proofpoint Isolation restricts dangerous sites by opening them in a secure container that disables uploads and downloads.
* If a safe site is flagged (false positive), look for the Isolation Banner at the top of the page.
* Click "Exit" to leave the isolated environment.
* The site will reload in the standard browser view.

#### 7. Printer Low Ink Alerts
**Intent:** Use this when a user reports a printer is low on ink.
* The printer system detects low ink levels and triggers an automatic response.
* A replacement ink order is initiated automatically with HP. No action is required by the user.

---

### 🛑 ESCALATION PROCEDURES (DO NOT TROUBLESHOOT)

**ESCALATION 1: ACE and MAGIC System Logins**
* **Trigger:** The user asks to reset an ACE or MAGIC password or needs access.
* **Action:** State that the MDA does not have access to ACE or MAGIC systems and cannot reset these passwords.
* **Resolution:** Direct the user to contact the Department of Finance and Administration (DFA) at 601-359-1343 or mash@dfa.ms.gov.

**ESCALATION 2: Desk Phone Issues**
* **Trigger:** The user asks for help with a physical desk phone.
* **Action:** State that desk phone inquiries are handled by the Operations Division.
* **Resolution:** Direct the user to contact Amanda Hughes at 601-359-2909 or ahughes@mississippi.org.

**ESCALATION 3: Active Directory Account Unlocks & Password Resets**
* **Trigger:** A user is completely locked out of their computer or needs their Active Directory password reset from the backend.
* **Action:** State that these changes require Administrative privileges.
* **Resolution (If User is an Admin):** Run Active Directory as an administrator > MDA local > Search user > Right-click user > Reset password (or go to Properties > Accounts > Unlock account).
* **Resolution (If User is NOT an Admin):** Route the user to open a support ticket for an IT administrator to assist them.