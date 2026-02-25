const nodemailer = require('nodemailer');

export default async function handler(req, res) {
  // Only allow POST
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { first_name, last_name, email, topic, message } = req.body;

  // Basic validation
  if (!first_name || !last_name || !email || !topic || !message) {
    return res.status(400).json({ error: 'All fields are required.' });
  }

  // Topic labels for the email
  const topicLabels = {
    support: 'App support / bug report',
    feature: 'Feature request',
    account: 'Account & billing',
    press: 'Press & media',
    partnership: 'Partnership',
    other: 'Other',
  };

  const topicLabel = topicLabels[topic] || topic;

  // Create transporter using SMTP env vars
  const transporter = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT, 10),
    secure: true, // true for port 465 (implicit TLS)
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
  });

  try {
    await transporter.sendMail({
      from: `"Itinirare Contact" <${process.env.SMTP_USER}>`,
      to: process.env.SMTP_TO,
      replyTo: `"${first_name} ${last_name}" <${email}>`,
      subject: `[${topicLabel}] Message from ${first_name} ${last_name}`,
      text: `Name: ${first_name} ${last_name}\nEmail: ${email}\nTopic: ${topicLabel}\n\n${message}`,
      html: `
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 600px; margin: 0 auto; padding: 32px 24px; color: #0f172a;">
          <div style="margin-bottom: 24px;">
            <img src="https://itinirare.com/favicon.png" alt="Itinirare" width="32" height="32" style="border-radius: 8px; vertical-align: middle; margin-right: 10px;">
            <span style="font-size: 1.1rem; font-weight: 700; vertical-align: middle;">Itinirare</span>
          </div>
          <h2 style="font-size: 1.2rem; font-weight: 700; margin: 0 0 20px; padding-bottom: 16px; border-bottom: 1px solid #e2e8f0;">
            New message from the contact form
          </h2>
          <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px;">
            <tr>
              <td style="padding: 8px 0; color: #64748b; font-size: 0.85rem; width: 120px; vertical-align: top;">Name</td>
              <td style="padding: 8px 0; font-weight: 600; font-size: 0.9rem;">${first_name} ${last_name}</td>
            </tr>
            <tr>
              <td style="padding: 8px 0; color: #64748b; font-size: 0.85rem; vertical-align: top;">Email</td>
              <td style="padding: 8px 0; font-size: 0.9rem;"><a href="mailto:${email}" style="color: #0d9488;">${email}</a></td>
            </tr>
            <tr>
              <td style="padding: 8px 0; color: #64748b; font-size: 0.85rem; vertical-align: top;">Topic</td>
              <td style="padding: 8px 0; font-size: 0.9rem;">${topicLabel}</td>
            </tr>
          </table>
          <div style="background: #f8fafc; border-radius: 12px; padding: 20px; font-size: 0.9rem; line-height: 1.7; white-space: pre-wrap;">${message.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</div>
          <p style="margin-top: 24px; font-size: 0.8rem; color: #94a3b8;">Reply directly to this email to respond to ${first_name}.</p>
        </div>
      `,
    });

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('SMTP error:', err);
    return res.status(500).json({ error: 'Failed to send message. Please try again later.' });
  }
}
