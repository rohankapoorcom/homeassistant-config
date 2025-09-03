# Notifications Package Documentation

## Overview
The notifications package manages comprehensive notification systems including text messaging, email, voice notifications, and mobile app notifications. This package provides a unified notification platform with multiple delivery methods, automated alerts for critical events, and intelligent notification routing across multiple devices.

## Configuration Files
- `packages/notifications.yaml`: Main notifications configuration

## Functionality
The notifications package provides:
- **Multi-Platform Notifications**: Email, mobile app, and voice notifications
- **Unified Notification Service**: Group notification service for multiple delivery methods
- **Automated Alerts**: Battery warnings and leak detection notifications
- **Text-to-Speech**: Google Translate TTS integration for voice notifications
- **Email Integration**: Mailgun email service for reliable email delivery
- **Mobile App Support**: Multiple mobile device notification support

## Key Components

### Notification Services
- **Email Service**: Mailgun integration for reliable email delivery
- **Mobile App Notifications**: Multiple mobile device support
- **Voice Notifications**: Text-to-speech for audio alerts
- **Group Notifications**: Unified service for multiple delivery methods

### Automated Alert System
- **Battery Monitoring**: Low battery detection and notifications
- **Leak Detection**: Water leak sensor alerts
- **Intelligent Filtering**: Exclusion of specific devices from alerts
- **Template-Based Messages**: Dynamic notification content

### Delivery Methods
- **Email**: Professional email notifications via Mailgun
- **Mobile Apps**: Direct notifications to multiple mobile devices
- **Voice**: Text-to-speech audio notifications
- **Multi-Device**: Simultaneous delivery to all registered devices

## Entities

### Notification Services
- `notify.rohan_email`: Email notification service via Mailgun
  - **Platform**: Mailgun
  - **Recipient**: Configured email recipient
  - **Sender**: Configured email sender

- `notify.rohan_kapoor`: Group notification service
  - **Services**: Email, mobile apps, voice
  - **Devices**: Multiple mobile devices and email
  - **Delivery**: Simultaneous delivery to all services

### Text-to-Speech
- **Platform**: Google Translate TTS
- **Integration**: Voice notification support
- **Language**: Configurable language support

### Mobile App Services
- `notify.mobile_app_rohan_s_oneplus_8_pro`: OnePlus 8 Pro notifications
- `notify.mobile_app_rohans_ipad_pro_5th_generation`: iPad Pro 5th gen notifications
- `notify.mobile_app_rohans_ipad_pro_6th_gen`: iPad Pro 6th gen notifications
- `notify.mobile_app_rohan_s_samsung_z_fold_4`: Samsung Z Fold 4 notifications

## Automations

### Low Battery Warnings
- **ID**: `1665347764581`
- **Description**: Automated low battery detection and notification
- **Blueprint**: `low-battery-level-detection-notification-for-all-battery-sensors.yaml`
- **Functionality**:
  - **Battery Monitoring**: Monitors all battery sensors for low levels
  - **Intelligent Filtering**: Excludes specific devices from monitoring
  - **Dynamic Messages**: Creates personalized notification messages
  - **Multi-Device Delivery**: Sends notifications to all registered devices

### Leak Warnings
- **ID**: `4143de0d-c3b5-4e86-9076-ee7422cbf0d6`
- **Description**: Water leak detection and emergency notification
- **Blueprint**: `leak-detector-notifier.yaml`
- **Functionality**:
  - **Leak Detection**: Monitors water leak sensors
  - **Emergency Alerts**: Immediate notification for water leaks
  - **Device Identification**: Includes sensor name in notification
  - **Critical Priority**: High-priority notification delivery

## Dependencies
- **Mailgun**: Email service integration
- **Google Translate TTS**: Text-to-speech functionality
- **Mobile App Integration**: Mobile device notification support
- **Custom Blueprints**: Battery monitoring and leak detection blueprints
- **Secrets Management**: Secure API key and credential storage

## Usage
The notifications package provides several interaction methods:
- **Automated Alerts**: Automatic notifications for critical events
- **Manual Notifications**: Direct notification service calls
- **Voice Commands**: Voice notification support
- **Email Integration**: Professional email notifications
- **Mobile App Integration**: Direct mobile device notifications

## Configuration

### Mailgun Setup
- **Domain**: Configured Mailgun domain
- **API Key**: Secure API key storage
- **Recipient**: Email recipient configuration
- **Sender**: Email sender configuration

### Mobile App Configuration
- **Device Registration**: Multiple mobile device support
- **App Integration**: Home Assistant mobile app integration
- **Notification Channels**: Configurable notification channels

### Blueprint Integration
- **Battery Monitoring**: Custom blueprint for battery level detection
- **Leak Detection**: Custom blueprint for water leak monitoring
- **Template Logic**: Dynamic message generation

## Related Files
- `packages/notifications.yaml`: Main notifications package configuration
- `blueprints/automation/rohankapoorcom/low-battery-level-detection-notification-for-all-battery-sensors.yaml`: Battery monitoring blueprint
- `blueprints/automation/TurtleFX/leak-detector-notifier.yaml`: Leak detection blueprint
- `secrets.yaml`: Secure credential storage

## Notes
- Notifications use secure credential storage via secrets.yaml
- Battery monitoring excludes specific devices to reduce notification noise
- Leak detection provides immediate emergency notifications
- Multi-device delivery ensures notifications reach all registered devices
- Voice notifications support multiple languages via Google Translate
- Email notifications use professional Mailgun service for reliability
- Custom blueprints provide sophisticated notification logic and filtering
