<?php
/**
 * 4 Seasons Cleaning - Contact Form Handler
 * Mijndomein.nl Hosting Configuration
 * Email: info@4seasonscleaning.be
 */

// Security headers
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('X-XSS-Protection: 1; mode=block');

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit(json_encode(['success' => false, 'message' => 'Method not allowed']));
}

// Validate form data
$name = sanitize_input($_POST['name'] ?? '');
$email = sanitize_input($_POST['email'] ?? '');
$phone = sanitize_input($_POST['phone'] ?? '');
$service = sanitize_input($_POST['service'] ?? '');
$message = sanitize_input($_POST['message'] ?? '');

// Validation checks
$errors = [];

if (empty($name)) {
    $errors[] = 'Naam is verplicht';
}

if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'Geldig e-mailadres is verplicht';
}

if (empty($phone)) {
    $errors[] = 'Telefoonnummer is verplicht';
}

if (empty($service)) {
    $errors[] = 'Service selectie is verplicht';
}

if (empty($message)) {
    $errors[] = 'Bericht is verplicht';
}

// Return validation errors
if (!empty($errors)) {
    http_response_code(400);
    exit(json_encode([
        'success' => false,
        'message' => implode(', ', $errors)
    ]));
}

// Prepare email
$recipient = 'info@4seasonscleaning.be';
$sender = 'no-reply@4seasonscleaning.be';
$subject = '4 Seasons - Nieuwe Offerteverzoek van ' . $name;

// Email body - HTML format
$email_body = build_email_body($name, $email, $phone, $service, $message);

// Email headers
$headers = [
    'From: ' . $sender,
    'Reply-To: ' . $email,
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=UTF-8',
    'X-Mailer: 4 Seasons PHP Mailer'
];

// Send email
$mail_sent = mail($recipient, $subject, $email_body, implode("\r\n", $headers));

if ($mail_sent) {
    // Log successful submission
    log_submission($name, $email, $phone, $service, $message);
    
    http_response_code(200);
    exit(json_encode([
        'success' => true,
        'message' => 'Bedankt! We nemen snel contact met je op.'
    ]));
} else {
    http_response_code(500);
    exit(json_encode([
        'success' => false,
        'message' => 'Er is iets misgegaan bij het verzenden. Probeer later opnieuw.'
    ]));
}

/**
 * Sanitize input to prevent XSS
 */
function sanitize_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data, ENT_QUOTES, 'UTF-8');
    return $data;
}

/**
 * Build HTML email body
 */
function build_email_body($name, $email, $phone, $service, $message) {
    $timestamp = date('d-m-Y H:i:s');
    
    return <<<HTML
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0; padding: 20px; background-color: #f9fafb; }
        .header { background-color: #1e3a5f; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }
        .header h1 { margin: 0; font-size: 24px; }
        .content { background-color: white; padding: 20px; }
        .field { margin-bottom: 15px; border-bottom: 1px solid #e5e7eb; padding-bottom: 15px; }
        .field:last-child { border-bottom: none; }
        .label { font-weight: bold; color: #1e3a5f; font-size: 12px; text-transform: uppercase; }
        .value { margin-top: 5px; color: #555; }
        .footer { background-color: #f3f4f6; padding: 15px; text-align: center; font-size: 12px; color: #666; border-radius: 0 0 5px 5px; }
        .timestamp { color: #999; font-size: 11px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧹 Nieuw Offerteverzoek</h1>
            <p>4 Seasons Cleaning</p>
        </div>
        
        <div class="content">
            <div class="field">
                <div class="label">Naam</div>
                <div class="value">{$name}</div>
            </div>
            
            <div class="field">
                <div class="label">E-mailadres</div>
                <div class="value"><a href="mailto:{$email}">{$email}</a></div>
            </div>
            
            <div class="field">
                <div class="label">Telefoonnummer</div>
                <div class="value"><a href="tel:{$phone}">{$phone}</a></div>
            </div>
            
            <div class="field">
                <div class="label">Gevraagde Service</div>
                <div class="value">{$service}</div>
            </div>
            
            <div class="field">
                <div class="label">Bericht</div>
                <div class="value">{$message}</div>
            </div>
        </div>
        
        <div class="footer">
            <p>Ingediend op: <span class="timestamp">{$timestamp}</span></p>
            <p>Dit is een geautomatiseerd bericht. Reageer rechtstreeks aan: {$email}</p>
        </div>
    </div>
</body>
</html>
HTML;
}

/**
 * Log submission to file for backup
 */
function log_submission($name, $email, $phone, $service, $message) {
    $log_file = __DIR__ . '/logs/form_submissions.log';
    
    // Create logs directory if it doesn't exist
    if (!is_dir(__DIR__ . '/logs')) {
        @mkdir(__DIR__ . '/logs', 0755, true);
    }
    
    $timestamp = date('Y-m-d H:i:s');
    $log_entry = "[{$timestamp}] Name: {$name} | Email: {$email} | Phone: {$phone} | Service: {$service}\n";
    $log_entry .= "Message: " . substr($message, 0, 100) . "...\n";
    $log_entry .= str_repeat("-", 80) . "\n";
    
    @file_put_contents($log_file, $log_entry, FILE_APPEND);
}
?>
