# Home Assistant Configuration Rules & Guidelines

## 🚨 CRITICAL RULES (AI MUST FOLLOW)

### Home Assistant Compliance Requirements
- **ALWAYS follow [Home Assistant documentation](https://www.home-assistant.io/docs/)** for all configurations
- **ALWAYS ensure automations comply** with [Home Assistant automation standards](https://www.home-assistant.io/docs/automation/)
- **ALWAYS follow [Home Assistant YAML syntax](https://www.home-assistant.io/docs/configuration/yaml/)** for all configuration files
- **ALWAYS use [Home Assistant blueprints](https://www.home-assistant.io/docs/automation/blueprints/)** when available instead of custom automations
- **ALWAYS follow [Home Assistant package structure](https://www.home-assistant.io/docs/configuration/packages/)** for modular organization
- **ALWAYS use [Home Assistant templating](https://www.home-assistant.io/docs/configuration/templating/)** syntax correctly
- **ALWAYS follow [Home Assistant entity naming](https://www.home-assistant.io/docs/configuration/devices/)** conventions

### Security Requirements
- **NEVER commit `secrets.yaml`** or real API keys to version control
- **NEVER hardcode passwords** or sensitive data in configuration files
- **ALWAYS use `!secret`** references in configuration files
- **ALWAYS store test secrets** in `tests/travis_secrets.yaml` for validation

### Testing Requirements
- **ALWAYS run `./tests/test-config.sh`** before committing any changes
- **ALWAYS fix yamllint errors** before pushing to repository
- **ALWAYS test against your current HA version** (2025.1.1)
- **ALWAYS verify GUID uniqueness** across all entities

### ID Field Requirements
- **ALWAYS use GUIDs** for `id` fields in automations, scripts, template entities, groups, etc.
- **ALWAYS generate GUIDs** using [GUID Generator](https://www.guidgenerator.com/) or similar tools
- **ALWAYS use hyphenated format** (e.g., `550e8400-e29b-41d4-a716-446655440000`)
- **NEVER reuse GUIDs** - each entity must have a unique identifier
- **ALWAYS document GUIDs** in comments when creating multiple related entities

## 📝 AI WORKFLOW INSTRUCTIONS

### Before Making Changes
1. **Run validation**: Execute `./tests/test-config.sh` to ensure current state works
2. **Check dependencies**: Verify all required integrations and components are available
3. **Create feature branch**: Use `git checkout -b feature/descriptive-name` for significant changes

### During Development
1. **Follow naming conventions**: Use snake_case for files, descriptive names for packages
2. **Use proper YAML formatting**: 2-space indentation, consistent spacing, quote strings when needed
3. **Generate GUIDs**: Use [GUID Generator](https://www.guidgenerator.com/) for all ID fields
4. **Document changes**: Add comments explaining complex logic or non-standard configurations

### Before Committing
1. **Run full validation**: Execute `./tests/test-config.sh`
2. **Check yamllint**: Execute `yamllint .` and fix any errors
3. **Verify GUIDs**: Ensure all ID fields use proper GUIDs and are unique
4. **Test automations**: Verify automations work in safe environment
5. **Update documentation**: Follow `.ai/prompts/homeassistant-documentation.xml` standards
6. **Use automation prompt**: Follow `.ai/prompts/homeassistant-automation-creation.xml` for new automations

## 🏗️ PROJECT STRUCTURE RULES

### Directory Organization (AI MUST FOLLOW)
- **`packages/`**: Modular configuration packages (e.g., `notifications.yaml`, `security.yaml`)
- **`custom_components/`**: Custom integrations and components
- **`blueprints/`**: Automation blueprints for reusability
- **`themes/`**: Custom UI themes
- **`www/`**: Static web assets
- **`groups/`**: Entity grouping configurations
- **`dashboards/`**: Lovelace dashboard configurations
- **`tests/`**: Testing scripts and test secrets
- **`python_scripts/`**: Python scripts for advanced automation
- **`shell_command/`**: Shell command definitions
- **`bash_scripts/`**: Bash scripts for system operations

### File Naming Conventions (AI MUST FOLLOW)
- **Use snake_case** for all YAML files
- **Use descriptive names** that indicate purpose (e.g., `security.yaml`, `notifications.yaml`)
- **Keep main configuration** in `configuration.yaml`
- **Use package includes** for modular organization

## 📝 CONFIGURATION STANDARDS (AI MUST FOLLOW)

### Home Assistant YAML Standards
- **ALWAYS follow [Home Assistant YAML syntax](https://www.home-assistant.io/docs/configuration/yaml/)** requirements
- **ALWAYS use proper [Home Assistant templating](https://www.home-assistant.io/docs/configuration/templating/)** syntax
- **ALWAYS follow [Home Assistant entity naming](https://www.home-assistant.io/docs/configuration/devices/)** conventions
- **ALWAYS use [Home Assistant package structure](https://www.home-assistant.io/docs/configuration/packages/)** for modular organization

### YAML Formatting Rules
- **Indent with 2 spaces** (never tabs)
- **Use consistent spacing** around colons and dashes
- **Quote strings** when they contain special characters or spaces
- **Use anchors and aliases** (`&anchor`, `*alias`) for repeated values
- **Group related configurations** logically

### Package Structure Template (AI MUST USE)
```yaml
---
homeassistant:
  customize:
    package.node_anchors:
      customize: &customize
        package: 'package_name'

# Package-specific configurations
# (integrations, automations, scripts, etc.)
```

### Automation Structure Template (AI MUST USE)
```yaml
automation:
  - id: '550e8400-e29b-41d4-a716-446655440000'  # Generated GUID
    alias: 'Descriptive Name'
    description: 'What this automation does'
    use_blueprint:
      path: 'blueprint_path.yaml'
      input:
        # Blueprint inputs
```

## 🚫 PROHIBITED PRACTICES (AI MUST NEVER DO)

### Security Violations
- ❌ **NEVER commit real API keys** or passwords to version control
- ❌ **NEVER hardcode sensitive data** in configuration files
- ❌ **NEVER expose internal network details** in public repositories
- ❌ **NEVER commit `secrets.yaml`** (if using local secrets)

### Configuration Violations
- ❌ **NEVER use deprecated features** without migration plan
- ❌ **NEVER use hardcoded IP addresses** (use hostnames or DHCP)
- ❌ **NEVER mix different configuration styles** in the same file
- ❌ **NEVER create overly complex automations** without documentation
- ❌ **NEVER use simple strings** for ID fields (always use GUIDs)
- ❌ **NEVER reuse GUIDs** across different entities
- ❌ **NEVER deviate from [Home Assistant documentation](https://www.home-assistant.io/docs/)** standards
- ❌ **NEVER use non-standard YAML syntax** not supported by Home Assistant

### Code Quality Violations
- ❌ **NEVER ignore yamllint warnings** without justification
- ❌ **NEVER create duplicate configurations** across packages
- ❌ **NEVER commit broken configurations** (even temporarily)
- ❌ **NEVER use sequential IDs** or simple strings for entity identification

## ✅ REQUIRED PRACTICES (AI MUST ALWAYS DO)

### Documentation Requirements
- **ALWAYS follow** the comprehensive documentation prompt in `.ai/prompts/homeassistant-documentation.xml`
- **ALWAYS use** the automation creation prompt in `.ai/prompts/homeassistant-automation-creation.xml` for creating new automations
- **ALWAYS document custom integrations** and their purposes with proper attribution
- **ALWAYS explain complex automations** with comments and use cases
- **ALWAYS keep README.md updated** with current custom components and their purposes
- **ALWAYS document non-standard configurations** and their rationale
- **ALWAYS create package documentation** in `docs/packages/` directory
- **ALWAYS create automation documentation** in `docs/automations/` directory
- **ALWAYS include blueprint documentation** with import buttons and usage examples
- **ALWAYS maintain alphabetical ordering** in all component lists for easy reference
- **ALWAYS verify component links** by checking HACS default repositories for accuracy

### Testing Requirements
- **ALWAYS test all changes locally** before committing
- **ALWAYS validate against multiple HA versions** when possible
- **ALWAYS test automations** in a safe environment first
- **ALWAYS verify integrations** work as expected
- **ALWAYS verify GUID uniqueness** across all entities

### Maintenance Requirements
- **ALWAYS keep dependencies updated** (custom components, etc.)
- **ALWAYS review and clean up** unused configurations
- **ALWAYS monitor for deprecation warnings** and plan migrations
- **ALWAYS test the full configuration** regularly

## 🔄 AUTOMATION GUIDELINES (AI MUST FOLLOW)

### Home Assistant Automation Standards
- **ALWAYS follow [Home Assistant automation documentation](https://www.home-assistant.io/docs/automation/)** for all automations
- **ALWAYS use [Home Assistant blueprints](https://www.home-assistant.io/docs/automation/blueprints/)** when available instead of custom automations
- **ALWAYS follow [Home Assistant automation triggers](https://www.home-assistant.io/docs/automation/trigger/)** syntax
- **ALWAYS follow [Home Assistant automation conditions](https://www.home-assistant.io/docs/automation/condition/)** syntax
- **ALWAYS follow [Home Assistant automation actions](https://www.home-assistant.io/docs/automation/action/)** syntax
- **ALWAYS use [Home Assistant automation templates](https://www.home-assistant.io/docs/automation/templating/)** correctly

### Best Practices
- **ALWAYS use blueprints** for common automation patterns
- **ALWAYS keep automations focused** on single responsibilities
- **ALWAYS use descriptive names** and aliases
- **ALWAYS add comments** for complex logic
- **ALWAYS test automations** before deployment

## 🏠 INTEGRATION STANDARDS (AI MUST FOLLOW)

### Custom Components
- **ALWAYS place in `custom_components/`** directory
- **ALWAYS follow Home Assistant naming conventions**
- **ALWAYS include proper error handling**
- **ALWAYS document integration requirements**
- **ALWAYS test thoroughly** before deployment

### Third-party Integrations
- **ALWAYS prefer official integrations** when available
- **ALWAYS document custom integrations** and their sources
- **ALWAYS keep track of updates** and compatibility
- **ALWAYS have fallback plans** for critical integrations





## 📋 AI VALIDATION CHECKLIST

### Before Committing (AI MUST VERIFY)
- [ ] **Local testing passes** (`./tests/test-config.sh`)
- [ ] **yamllint passes** without errors
- [ ] **No secrets** committed to repository
- [ ] **Documentation updated** following `.ai/prompts/homeassistant-documentation.xml` standards
- [ ] **Automations tested** in safe environment
- [ ] **Integration compatibility** verified
- [ ] **GUIDs used** for all ID fields and verified as unique

### Quick Validation (AI MUST CHECK)
- [ ] **Local testing passes** (`./tests/test-config.sh`)
- [ ] **yamllint passes** without errors
- [ ] **No secrets** committed to repository
- [ ] **Documentation updated** following `.ai/prompts/homeassistant-documentation.xml` standards
- [ ] **Automations tested** in safe environment
- [ ] **GUIDs used** for all ID fields

## 🎯 QUALITY STANDARDS (AI MUST MAINTAIN)

### Code Quality
- **ALWAYS use consistent formatting** and style
- **ALWAYS use clear and descriptive names**
- **ALWAYS include proper error handling**
- **ALWAYS perform comprehensive testing**

### Documentation Standards
- **ALWAYS follow** the comprehensive documentation prompt in `.ai/prompts/homeassistant-documentation.xml`
- **ALWAYS use** the automation creation prompt in `.ai/prompts/homeassistant-automation-creation.xml` for creating new automations
- **ALWAYS keep README.md updated** with current custom components and their purposes
- **ALWAYS provide clear setup instructions** and troubleshooting guides
- **ALWAYS maintain change logs** for major updates
- **ALWAYS create comprehensive package documentation** in `docs/packages/` directory
- **ALWAYS create detailed automation documentation** in `docs/automations/` directory
- **ALWAYS include blueprint documentation** with import buttons and usage examples
- **ALWAYS provide proper attribution** to original authors and source repositories
- **ALWAYS maintain alphabetical ordering** in all component lists for easy reference
- **ALWAYS verify component links** from HACS default repositories

### Performance Standards
- **ALWAYS create efficient automations**
- **ALWAYS optimize database usage**
- **ALWAYS use reasonable update intervals**
- **ALWAYS monitor resource usage**

## ⚠️ COMMON MISTAKES & SOLUTIONS (AI MUST AVOID)

### Don't Do This
- ❌ Commit without testing
- ❌ Ignore yamllint warnings
- ❌ Use hardcoded IP addresses
- ❌ Create overly complex automations
- ❌ Forget to document changes
- ❌ Use simple strings for ID fields
- ❌ Reuse GUIDs across entities

### Do This Instead
- ✅ Test locally first
- ✅ Fix all linting issues
- ✅ Use hostnames or DHCP
- ✅ Break complex automations into smaller ones
- ✅ Add comments and documentation
- ✅ Use GUIDs for all ID fields
- ✅ Generate unique GUIDs for each entity

## 🔧 COMMON COMMANDS (AI MUST USE)

### Testing Commands
```bash
# Full validation
./tests/test-config.sh

# Just yamllint
yamllint .

# Manual HA check
docker run --rm -v "$(pwd):/config" -v "$(pwd)/tests/travis_secrets.yaml:/config/secrets.yaml:ro" "ghcr.io/home-assistant/home-assistant:stable" python -m homeassistant --config /config --script check_config
```

### Git Workflow Commands
```bash
# Create feature branch
git checkout -b feature/new-integration

# Test before committing
./tests/test-config.sh

# Commit with description
git commit -m "Add new security integration with proper testing"

# Push and create PR
git push origin feature/new-integration
```

---

*These rules ensure consistency, security, and maintainability of your Home Assistant configuration. AI assistants MUST follow these rules to maintain a high-quality, reliable smart home setup.*
