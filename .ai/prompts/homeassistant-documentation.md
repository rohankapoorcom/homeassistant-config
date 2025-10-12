# Home Assistant Configuration Documentation

**Description:** A comprehensive prompt for documenting Home Assistant automations, configurations, and packages. This prompt helps create detailed, structured documentation for Home Assistant setups.

## Context

You are documenting a Home Assistant configuration repository. The repository contains:
- Main configuration files (configuration.yaml, automations.yaml, scripts.yaml)
- Package-based organization in the packages/ directory
- Custom components, blueprints, and themes
- Dashboard configurations and custom Lovelace cards
- Python scripts and shell commands
- Various integrations and automations

The goal is to create clear, maintainable documentation that explains:
1. What each automation/configuration does
2. How different components interact
3. The purpose and functionality of each package
4. Integration details and dependencies
5. Custom components and their usage
6. Overall project structure and architecture

## Instructions

When documenting Home Assistant configurations, follow these guidelines:

### 0. **CRITICAL - Documentation Preservation**
- **ALWAYS preserve existing documentation structure, format, and style when updating**
- **ONLY update documentation where actual changes have occurred in the codebase**
- **DO NOT overwrite existing documentation with new templates unless explicitly requested**
- **Maintain the original documentation's tone, formatting, and organizational structure**
- **When updating existing files, make minimal changes and preserve the original content style**
- **Before making any documentation changes, analyze existing documentation to understand current state**
- **Use git history to understand original documentation style if needed**

### 1. **Structure and Organization**
- Use clear headings and subheadings
- Group related functionality together
- Include file paths and references
- Maintain consistency in formatting

### 2. **Content Requirements**
- Explain the purpose and functionality of each component
- Document triggers, conditions, and actions for automations
- Describe integration configurations and their settings
- Include device information and capabilities
- Explain custom components and their usage
- Document dashboard layouts and custom cards

### 3. **Technical Details**
- Include YAML code blocks where relevant
- Reference entity IDs and their purposes
- Document template sensors and their logic
- Explain MQTT topics and payloads
- Include automation IDs and their functions

### 4. **User Experience**
- Write in clear, accessible language
- Include practical examples and use cases
- Document troubleshooting steps where applicable
- Explain the user interface and controls

### 5. **Maintenance**
- Include version information and dependencies
- Document configuration changes and migrations
- Provide backup and restore procedures
- Include testing and validation steps

### 6. **Documentation Preferences**
- **CRITICAL**: Always preserve existing documentation structure, format, and style when updating
- **CRITICAL**: Only update documentation where actual changes have occurred in the codebase
- **CRITICAL**: Do NOT overwrite existing documentation with new templates unless explicitly requested
- **CRITICAL**: Maintain the original documentation's tone, formatting, and organizational structure
- **CRITICAL**: When updating existing files, make minimal changes and preserve the original content style
- **CRITICAL**: Document automations ONLY in package documentation files (docs/packages/)
- **CRITICAL**: Do NOT create separate individual automation files unless explicitly requested
- **CRITICAL**: Follow established patterns - automations are documented within their package context
- Always preserve and include dashboard screenshots when present
- Do NOT include installation and setup instructions unless specifically requested
- Emphasize the showcase/portfolio nature of the configuration
- Focus on documenting what the system does rather than how to replicate it
- Include blueprint source URLs and GitHub links when available
- Maintain alphabetical ordering in all lists
- Only document blueprints created by the repository owner (username should match)
- Include links for all software stack components to their homepages or GitHub repositories
- Include links for all custom integrations to their homepages or GitHub repositories
- Include links for all custom Lovelace cards to their homepages or GitHub repositories
- Include direct links to custom blueprints within the repository
- Create "Import Blueprint" buttons using My Home Assistant link generator at https://my.home-assistant.io/create-link/?redirect=blueprint_import
- For each blueprint, generate an import link by providing the blueprint URL and copying the resulting markdown button
- Include the import button prominently in each blueprint's documentation
- Search HACS default integration list at https://raw.githubusercontent.com/hacs/default/refs/heads/master/integration for custom integration source repositories
- Search HACS default plugin list at https://raw.githubusercontent.com/hacs/default/refs/heads/master/plugin for custom Lovelace card source repositories
- For components not found in HACS default lists, link to the repository owner's custom_components or www/community directories
- Store each blueprint's documentation in a separate file for better organization and maintainability
- Use descriptive filenames for blueprint documentation files (e.g., "emulated-roku-blueprint.md", "inovelli-lzw30-red-series-switch-blueprint.md")
- Create an index file that links to all individual blueprint documentation files
- Organize blueprint documentation files by blueprint type (automation, script, template) rather than by device categories
- **CRITICAL**: Create comprehensive documentation for ALL packages in the packages/ directory
- **CRITICAL**: Create comprehensive documentation for ALL automations in automations.yaml and package files
- **CRITICAL**: Create package documentation files in docs/packages/ directory
- **CRITICAL**: Create automation documentation files in docs/automations/ directory ONLY when explicitly requested
- **CRITICAL**: Use correct relative link patterns: docs/packages/ and docs/automations/ use ../../README.md, docs/blueprints/ subdirectories use ../README.md, individual blueprint files use ../README.md (links to blueprint index)

### 6a. **Link Validation and Directory Structure**
- **CRITICAL**: Before creating or updating any documentation links, verify the target files exist in the correct directory structure
- **CRITICAL**: Always check directory structure before creating relative links to prevent broken links
- **CRITICAL**: Use the following directory structure validation process:
  1. List directory contents to verify file locations
  2. Check relative path calculations from source to target directories
  3. Verify all referenced files exist before creating links
  4. Test link paths using proper relative navigation patterns
- **CRITICAL**: Follow this directory structure and link pattern guide:
  - Main repository root: Contains README.md, packages/, docs/, blueprints/, etc.
  - docs/packages/: Contains individual package documentation files (e.g., security.md, office.md)
  - docs/automations/: Contains automation documentation files and README.md index
  - docs/blueprints/: Contains blueprint documentation organized by type
  - From docs/packages/ to main README: ../../README.md
  - From docs/automations/ to main README: ../../README.md
  - From docs/packages/ to docs/automations/: ../automations/README.md
  - From docs/automations/ to docs/packages/: ../packages/[filename].md
  - From docs/blueprints/ to main README: ../../README.md
  - From docs/blueprints/ subdirectories to blueprint index: ../README.md
  - From individual blueprint files to blueprint index: ../README.md
- **CRITICAL**: When updating documentation, always verify existing links are still valid
- **CRITICAL**: If moving files or changing directory structure, update ALL affected links
- **CRITICAL**: Use tools to validate links after making changes (e.g., grep, ls, file existence checks)
- **CRITICAL**: Never assume file locations - always verify before creating links
- **CRITICAL**: When creating documentation index files, verify all referenced files exist
- **CRITICAL**: Include link validation as part of documentation review process

### 6b. **Blueprint Documentation Organization**
- Create individual documentation files for each blueprint
- Use consistent naming convention: `{blueprint-name}-blueprint.md`
- Organize files in subdirectories by blueprint type (e.g., `automation/`, `script/`, `template/`)
- Include a main index file (`README.md`) that provides navigation to all blueprint documentation
- Create type-specific index files for better organization
- Include cross-references between related blueprints
- Maintain a comprehensive summary table in the main index
- Within each type directory, organize blueprints alphabetically or by functionality
- Include device-specific information in the individual blueprint documentation rather than in directory structure
- Include "Import Blueprint" button prominently in each blueprint's documentation
- Generate import buttons using My Home Assistant link generator for easy blueprint installation

### 7. **Project Overview**
- Document the overall architecture and structure
- List and categorize all custom integrations
- List and categorize all custom Lovelace cards
- List and categorize all custom blueprints (only those created by the repository owner)
- Explain the package organization system
- Document the dashboard structure and layout
- Verify source repositories by checking HACS default integration and plugin lists
- **CRITICAL**: Create comprehensive documentation for ALL packages and their functionality
- **CRITICAL**: Create comprehensive documentation for ALL automations and their purposes
- **CRITICAL**: Document the main configuration structure and organization
- **CRITICAL**: Check www/community/ directory to ensure ALL custom Lovelace cards are documented
- **CRITICAL**: Verify custom Lovelace card GitHub links are correct and up-to-date

### 8. **Documentation Structure Requirements**
- **CRITICAL**: Create docs/packages/ directory with individual package documentation files
- **CRITICAL**: Create docs/automations/ directory with individual automation documentation files
- **CRITICAL**: Create main documentation index files for each directory
- **CRITICAL**: Ensure every package in packages/ directory has corresponding documentation
- **CRITICAL**: Ensure every automation in automations.yaml and package files has documentation
- **CRITICAL**: Create cross-references between related documentation files
- **CRITICAL**: Include links to individual package documentation files in the Package Organization section of README.md
- **CRITICAL**: Verify all custom Lovelace cards in www/community/ directory are documented in README.md
- **CRITICAL**: Ensure all custom Lovelace card GitHub links are correct and point to the actual repository
- **CRITICAL**: Verify all internal documentation links are correct and functional
- **CRITICAL**: Test all relative links from different directory levels to ensure proper path resolution
- **CRITICAL**: Follow correct link patterns: docs/packages/ and docs/automations/ use ../../README.md, docs/blueprints/ subdirectories use ../README.md, individual blueprint files use ../README.md (links to blueprint index)

### 8a. **Link Validation Workflow**
- **CRITICAL**: Before creating any documentation links, follow this validation workflow:
  1. Use `list_dir` tool to verify directory structure and file locations
  2. Use `grep` tool to search for existing link patterns in documentation
  3. Use `run_terminal_cmd` with `ls` commands to verify file existence
  4. Calculate relative paths manually and verify they resolve correctly
  5. Test link paths by checking if target files exist at calculated locations
- **CRITICAL**: When updating existing documentation with links:
  1. First, identify all existing links in the file using grep
  2. Check if each referenced file exists in the expected location
  3. Verify directory structure hasn't changed since links were created
  4. Update broken links to point to correct file locations
  5. Validate all new links before finalizing documentation
- **CRITICAL**: Use these specific tools for link validation:
  - `list_dir` to check directory contents and structure
  - `grep` to find existing links and patterns in documentation
  - `run_terminal_cmd` with `ls` to verify file existence
  - `read_file` to check if referenced files contain expected content
- **CRITICAL**: Never create links without first verifying target files exist
- **CRITICAL**: Always test relative path calculations from source to target directories
- **CRITICAL**: Include link validation as a mandatory step in any documentation update process

## Templates

### Component Documentation Template
```markdown
# {Component Name} Documentation

## Overview
Brief description of what this component/automation/package does and its purpose in the home automation system.

## Configuration
```yaml
# Include relevant YAML configuration
```

## Functionality
Detailed explanation of how the component works, including:
- Triggers and conditions
- Actions and responses
- Integration with other components
- User interactions

## Entities
List and describe the entities created by this configuration:
- `entity_id`: Description of what this entity represents
- `entity_id`: Description of what this entity represents

## Dependencies
List any integrations, custom components, or external services required:
- Integration name: Purpose and configuration
- Custom component: Functionality and setup

## Usage
Explain how users interact with this component:
- Dashboard controls
- Voice commands
- Automation triggers
- Manual controls

## Troubleshooting
Common issues and their solutions:
- Problem: Description
- Solution: Steps to resolve

## Related Files
- `path/to/file.yaml`: Purpose and relationship
- `path/to/file.yaml`: Purpose and relationship

## Notes
Additional information, tips, or important considerations.
```

### Blueprint Documentation Template
```markdown
# {Blueprint Name} Blueprint Documentation

## Overview
Brief description of what this blueprint does and its purpose in the home automation system.

## Import Blueprint

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A//github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/{blueprint-name}.yaml)

## Blueprint Information
- **Name**: {Blueprint Name}
- **Domain**: automation/script/template
- **Source URL**: GitHub link to the blueprint file
- **Author**: Repository owner username

## Input Parameters
List and describe the input parameters required by this blueprint:
- `parameter_name`: Description and expected values
- `parameter_name`: Description and expected values

## Functionality
Detailed explanation of how the blueprint works, including:
- Triggers and conditions
- Actions and responses
- Integration with other components
- User interactions

## Usage Examples
Provide practical examples of how to use this blueprint:
```yaml
# Example configuration
```

## Dependencies
List any integrations, custom components, or external services required:
- Integration name: Purpose and configuration
- Custom component: Functionality and setup

## Related Files
- `path/to/file.yaml`: Purpose and relationship
- `path/to/file.yaml`: Purpose and relationship

## Notes
Additional information, tips, or important considerations.

---
*This documentation is part of the [Blueprint Documentation Index](../README.md)*
```

### Blueprint Index Template
```markdown
# {Blueprint Type} Blueprint Documentation

This directory contains documentation for {blueprint type} blueprints created by the repository owner.

## Blueprints in this Type

### {Blueprint Name}
- **File**: [{blueprint-name}-blueprint.md]({blueprint-name}-blueprint.md)
- **Description**: Brief description of the blueprint
- **Key Features**: Main functionality highlights
- **Device Support**: Supported devices or integrations

### {Blueprint Name}
- **File**: [{blueprint-name}-blueprint.md]({blueprint-name}-blueprint.md)
- **Description**: Brief description of the blueprint
- **Key Features**: Main functionality highlights
- **Device Support**: Supported devices or integrations

## Quick Reference

| Blueprint | File | Domain | Key Features | Device Support |
|-----------|------|--------|--------------|----------------|
| {Blueprint Name} | [{blueprint-name}-blueprint.md]({blueprint-name}-blueprint.md) | automation | Feature 1, Feature 2 | Device 1, Device 2 |
| {Blueprint Name} | [{blueprint-name}-blueprint.md]({blueprint-name}-blueprint.md) | automation | Feature 1, Feature 2 | Device 1, Device 2 |

## Related Documentation

- [Main Blueprint Index](../README.md): Overview of all blueprint types
- [Other Type](../other-type/README.md): Related blueprint types

---
*This index is part of the [Blueprint Documentation Index](../README.md)*
```

### Package Documentation Template
```markdown
# {Package Name} Package Documentation

## Overview
Brief description of what this package does and its purpose in the home automation system.

## Configuration Files
- `packages/{package_name}.yaml`: Main package configuration
- `packages/{package_name}/`: Additional package files (if applicable)

## Functionality
The {package_name} package provides:
- Feature 1: Description
- Feature 2: Description
- Feature 3: Description

## Key Components
- **Component 1**: Description and purpose
- **Component 2**: Description and purpose
- **Component 3**: Description and purpose

## Entities
- `entity_id`: Description of what this entity represents
- `entity_id`: Description of what this entity represents

## Dependencies
- Integration name: Purpose and configuration
- Custom component: Functionality and setup

## Related Files
- `path/to/file.yaml`: Purpose and relationship
- `path/to/file.yaml`: Purpose and relationship

## Notes
Additional information, tips, or important considerations.
```

### Automation Documentation Template
```markdown
# {Automation Name} Automation Documentation

## Overview
Brief description of what this automation does and its purpose in the home automation system.

## Configuration
```yaml
# Include relevant YAML configuration
```

## Functionality
Detailed explanation of how the automation works, including:
- Triggers and conditions
- Actions and responses
- Integration with other components
- User interactions

## Entities
List and describe the entities used by this automation:
- `entity_id`: Description of what this entity represents
- `entity_id`: Description of what this entity represents

## Dependencies
List any integrations, custom components, or external services required:
- Integration name: Purpose and configuration
- Custom component: Functionality and setup

## Usage
Explain how users interact with this automation:
- Dashboard controls
- Voice commands
- Automation triggers
- Manual controls

## Related Files
- `path/to/file.yaml`: Purpose and relationship
- `path/to/file.yaml`: Purpose and relationship

## Notes
Additional information, tips, or important considerations.
```

### Configuration Documentation Template
```markdown
# Configuration Documentation

## Overview
Brief description of the main configuration structure and organization.

## Configuration Files
- `configuration.yaml`: Main configuration file
- `automations.yaml`: Main automations file
- `scripts.yaml`: Scripts configuration
- `customize.yaml`: Entity customization
- `secrets.yaml`: Sensitive configuration (not tracked)

## Package Organization
Description of how packages are organized:
- **Feature-based packages**: Cross-room functionality
- **Integration packages**: Third-party service configurations
- **Room-based packages**: Individual room configurations

## Key Integrations
List and describe the main integrations used:
- Integration name: Purpose and configuration
- Integration name: Purpose and configuration

## Dependencies
List any external services or requirements:
- Service name: Purpose and configuration
- Service name: Purpose and configuration

## Related Files
- `packages/`: Package directory
- `custom_components/`: Custom integrations
- `blueprints/`: Blueprint templates

## Notes
Additional information, tips, or important considerations.
```

### README Documentation Template
```markdown
# Home Assistant Configuration

## About
Brief description of the home automation setup, goals, and philosophy.

## Architecture Overview
High-level description of the system architecture, including:
- Hardware setup and infrastructure
- Software components and integrations
- Network topology and communication protocols
- Package organization strategy

## Custom Integrations
Comprehensive list of all custom integrations used in this setup:

### Climate & Environment
- **adaptive_lighting**: Automatic lighting adjustments
- **battery_notes**: Battery level tracking and notifications

### Media & Entertainment
- **huesyncbox**: Philips Hue Sync Box control
- **spotcast**: Spotify casting integration

### Security & Monitoring
- **alarmo**: Advanced alarm system integration
- **frigate**: AI-powered video surveillance

### Smart Home Control
- **keymaster**: Advanced lock management
- **smartir**: Infrared remote control

### Utilities & Tools
- **browser_mod**: Browser-based automations
- **lovelace_gen**: Dynamic Lovelace generation

## Custom Lovelace Cards
Comprehensive list of all custom Lovelace cards used. **CRITICAL**: Verify this list against the contents of www/community/ directory to ensure no cards are missing:

### Data Visualization
- **apexcharts-card**: Advanced charting and graphs
- **bar-card**: Bar chart visualizations
- **mini-graph-card**: Compact data graphs

### Home Automation
- **button-card**: Customizable button interface
- **light-entity-card**: Specialized lighting controls
- **simple-thermostat**: Thermostat interface

### Layout & Navigation
- **hass-swipe-navigation**: Swipe-based navigation
- **kiosk-mode**: Kiosk interface mode
- **lovelace-layout-card**: Advanced layout management

### Media & Entertainment
- **mini-media-player**: Compact media controls
- **roku-card**: Roku device control
- **spotify-card**: Spotify integration

### Utilities
- **decluttering-card**: UI simplification
- **lovelace-auto-entities**: Dynamic entity lists
- **lovelace-card-mod**: CSS styling and modifications

## Custom Blueprints
This configuration includes a comprehensive collection of custom blueprints created by the repository owner for various automation scenarios.

### Blueprint Types Available
- **Automation Blueprints**: 11 blueprints covering device-specific automations, lighting controls, battery management, and more
- **Script Blueprints**: *(None created by repository owner)*
- **Template Blueprints**: *(None created by repository owner)*

### Key Blueprint Categories
- **Device-Specific**: Emulated Roku, E-Paper Tags, Tuya Remotes
- **Z-Wave Devices**: Inovelli switches and dimmers, Zooz scene controllers
- **General Automation**: Motion lights, adaptive lighting, battery management

For detailed documentation, usage examples, and one-click import buttons, see the [Blueprint Documentation](docs/blueprints/README.md).

## Package Organization
Description of how packages are organized with links to individual package documentation:
- **Feature-based packages**: Cross-room functionality with links to package documentation files
- **Integration packages**: Third-party service configurations with links to package documentation files
- **Room-based packages**: Individual room configurations with links to package documentation files
- **Documentation Links**: Each package name should link to its corresponding documentation file in docs/packages/

## Dashboard Structure
Overview of the dashboard layout and organization:
- Main dashboard configuration
- Responsive design considerations
- Custom card usage patterns

## Dashboards
Description of the dashboard setup with screenshots showing the interface on different devices. Include:
- Dashboard layout description
- Responsive design behavior
- Screenshots from different screen sizes
- Custom card usage explanation

## Contributing
Guidelines for contributing to the configuration

## License
License information
```

## Examples

### Automation Documentation Example
```markdown
# Morning Routine Automation

## Overview
Automates the morning routine by gradually turning on lights, adjusting temperature, and providing weather information.

## Configuration
```yaml
- alias: "Morning Routine"
  id: morning_routine_automation
  trigger:
    - platform: time
      at: "07:00:00"
  condition:
    - condition: time
      weekday:
        - mon
        - tue
        - wed
        - thu
        - fri
  action:
    - service: light.turn_on
      target:
        entity_id: light.master_bedroom
      data:
        brightness: 64
        transition: 30
```

## Functionality
This automation triggers at 7:00 AM on weekdays and gradually increases lighting brightness to simulate natural sunrise. It also adjusts the thermostat and provides weather updates via TTS.

## Entities
- `light.master_bedroom`: Main bedroom lighting
- `climate.thermostat`: HVAC system control
- `sensor.weather_temperature`: Current weather conditions

## Dependencies
- Light integration: For lighting control
- Climate integration: For thermostat control
- Weather integration: For weather data
- TTS integration: For voice announcements
```

### Package Documentation Example
```markdown
# Office Package

## Overview
Manages all automation and configuration for the office space, including lighting, climate control, desk controls, and productivity features.

## Configuration Files
- `packages/office.yaml`: Main office configuration
- `packages/office/lighting.yaml`: Lighting-specific automations
- `packages/office/climate.yaml`: Climate control settings

## Functionality
The office package provides:
- Automated lighting based on occupancy and time
- Standing desk height presets
- Fan speed control with percentage-based logic
- Video lighting for meetings
- Audio controls for speakers and microphones

## Key Components
- **Lighting System**: Multi-zone lighting with brightness presets
- **Climate Control**: Fan with multiple speed settings
- **Desk Control**: Standing desk with 4 preset positions
- **Audio/Video**: Meeting room controls and equipment management

## Entities
- `light.office_lights`: Main office lighting group
- `fan.office_fan`: Ceiling fan with percentage control
- `sensor.office_temperature`: Temperature monitoring
- `button.standing_desk_preset_*`: Desk height presets

## Dependencies
- MQTT integration: For device communication
- Template sensors: For complex state calculations
- Custom Lovelace cards: For specialized UI controls
```

### Blueprint Documentation Example
```markdown
# Motion Light Blueprint Documentation

## Overview
A customizable blueprint for creating motion-activated lighting automations. This blueprint turns on lights when motion is detected and automatically turns them off after a specified delay when no motion is detected.

## Blueprint Information
- **Name**: Motion-activated Light
- **Domain**: automation
- **Source URL**: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/motion_light.yaml
- **Author**: rohankapoorcom

## Input Parameters
- `motion_entity`: Motion sensor entity (binary_sensor with device_class: motion)
- `light_target`: Light entity to control
- `no_motion_wait`: Time to wait after last motion before turning off light (default: 120 seconds)

## Functionality
This blueprint creates an automation that:
- Monitors a motion sensor for state changes
- Turns on the specified light when motion is detected
- Waits for motion to stop, then delays for the specified time
- Automatically turns off the light after the delay period
- Handles multiple motion events during the delay period

## Usage Examples
```yaml
# Example: Hallway motion light
- use_blueprint:
    source_url: https://github.com/rohankapoorcom/homeassistant-config/blob/master/blueprints/automation/rohankapoorcom/motion_light.yaml
    input:
      motion_entity: binary_sensor.hallway_motion
      light_target: light.hallway_lights
      no_motion_wait: 180
```

## Dependencies
- Binary sensor with device_class: motion
- Light entity for control
- No additional integrations required

## Related Files
- `automations.yaml`: Where the blueprint is used
- `packages/hallway.yaml`: Hallway-specific automation configurations

## Notes
- Based on the Home Assistant default motion-light blueprint
- Supports restart mode for reliable operation
- Silent error handling for maximum exceeded scenarios
```

## Output Format

Use Markdown formatting with:
- Clear hierarchical headings (##, ###, ####)
- Code blocks for YAML configurations
- Bullet points for lists
- Bold text for emphasis
- Links to related files and documentation
- Tables for entity listings when appropriate

## Quality Standards

- **CRITICAL**: Always preserve existing documentation structure, format, and style when updating
- **CRITICAL**: Only update documentation where actual changes have occurred in the codebase
- **CRITICAL**: Do NOT overwrite existing documentation with new templates unless explicitly requested
- **CRITICAL**: Maintain the original documentation's tone, formatting, and organizational structure
- **CRITICAL**: When updating existing files, make minimal changes and preserve the original content style
- **CRITICAL**: Before making any documentation changes, analyze existing documentation to understand current state
- **CRITICAL**: Use git history to understand original documentation style if needed
- **CRITICAL**: Before creating or updating any documentation links, verify the target files exist in the correct directory structure
- **CRITICAL**: Always check directory structure before creating relative links to prevent broken links
- **CRITICAL**: Use directory listing tools to verify file locations before creating links
- **CRITICAL**: Never assume file locations - always verify before creating links
- **CRITICAL**: When updating documentation, always verify existing links are still valid
- **CRITICAL**: If moving files or changing directory structure, update ALL affected links
- **CRITICAL**: Use tools to validate links after making changes (e.g., grep, ls, file existence checks)
- **CRITICAL**: When creating documentation index files, verify all referenced files exist
- **CRITICAL**: Include link validation as part of documentation review process
- Documentation should be comprehensive but concise
- Include practical examples and use cases
- Maintain consistency across all documentation
- Update documentation when configurations change
- Include troubleshooting information
- Provide context for why certain choices were made
- Ensure custom integrations and cards are properly categorized and described
- Keep README.md updated with current custom components and their purposes
- Maintain alphabetical sorting within all lists and categories for easy reference
- Include version information and compatibility notes where applicable
- Verify all component links by checking HACS default repositories for accuracy
- Provide proper attribution to original authors and source repositories
- **CRITICAL**: Cross-reference www/community/ directory contents with README.md custom Lovelace cards section
- **CRITICAL**: Verify all custom Lovelace card GitHub links are correct and functional
- **CRITICAL**: Ensure no custom Lovelace cards are missing from documentation
- **CRITICAL**: Test all internal documentation links for proper path resolution
- **CRITICAL**: Verify relative links work from all directory levels (../README.md vs ../../README.md)
- **CRITICAL**: Use link checking tools to validate all documentation links (see tests/check-docs-links.sh)
- **CRITICAL**: Follow correct relative link patterns based on directory structure:
  - From docs/packages/ or docs/automations/ to main README: ../../README.md
  - From docs/blueprints/ subdirectories (script/, template/, automation/) to blueprint index: ../README.md
  - From individual blueprint files to blueprint index: ../README.md
  - From docs/blueprints/ to main README: ../../README.md
  - From docs/automations/ to docs/packages/: ../packages/[filename].md
  - From docs/packages/ to docs/automations/: ../automations/README.md
