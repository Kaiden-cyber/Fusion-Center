<h1>What is the Purpose?</h1>
<ul>
  <li><strong>Real-Time Threat Monitoring</strong> – Displays immediate security risks, categorized by severity</li>
  <li><strong>Multi-Agency Collaboration</strong> – Enables cross-department data sharing, ensuring law enforcement, cybersecurity teams, and financial regulators work with the same intelligence.</li>
  <li><strong>Automated Alerts & Reporting</strong> – Flags suspicious activities based on predefined criteria, ensuring high-risk events trigger swift responses.</li>
  <li><strong>Social Media Surveillance</strong> – Monitors posts linked to flagged individuals, identifying trends and key interactions.</li>
  <li><strong>Profile Tracking</strong> – Allows analysts to review historical behavior and predict future risks</li>
</ul>

<h1>What Features Does the Demo Include?</h1>

<p>Note: The demo is not a fully functioning version, as it has not been connected with any OSINT or social media sources to provide live alerts</p>
<h3>The Features:</h3>
<ul>
  <li>Categorises flagged individuals by risk level and sorts them accordingly</li>
  <li>Contains an example of social media post tracking(posts are not updated because the program has not been connected with those servcies)</li>
  <li>Profile Pages for each individual</li>
  <li>Allows you to upload new threats and add notes and social media profiles to the platform</li>
  <li>Contains a dashboard which updates with new data every 10 seconds and rotates between profiles and social media psots</li>
</ul>

<h1>How Far Away From the Finished Product is This Demo?</h1>
<p>This demo is suprisingly close to the actual dashboard that would be used in a cyber intelligence fusion center. The only thing missing is connecting python to APIs and library such as the Facebook and Twitter API and other OSINT sources. After those services have been connected, the data just needs to be cleaned up into the format that the demo uses, and it should be a fully fucnitoning and live updating threat intelligence dashboard.</p>

<h1>How to Run the Demo:</h1>
<p>The program just uses Flask to connect python to the HTML, so it is simple to run</p>
<ol>
  <li>download the Dashboard folder</li>
  <li>Navigate to the directory in your terminal</li>
  <li>Run: <i>pip install -r requirements.txt</i> to install the libraries that this project uses</li>
  <li>Run <i>python fusion_center.py</i></li>
  <li>Navigate to 127.0.0.1:5000 to see the program</li>
</ol>
<h2>When You Run the Program it Should Look Like This:</h2>

![Dashboard Preview](https://github.com/Kaiden-cyber/Fusion-Center/blob/398cde5e091787031337151f12e0fd4045c9bdbb/Dashboard/Demo.png)
