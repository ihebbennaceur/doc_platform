# PlantUML Diagram Viewing Guide

## Overview
All module diagrams are created in **PlantUML** format (`.puml` files). This guide shows how to view, render, and work with these diagrams.

## What is PlantUML?

PlantUML is a text-based diagram language that allows you to create UML diagrams using simple syntax. All diagrams in this project are written in PlantUML format.

**Benefits:**
- ✅ Version control friendly (plain text)
- ✅ No proprietary software needed
- ✅ Easy to edit and update
- ✅ Multiple rendering options

---

## Option 1: VS Code (Recommended)

### Install PlantUML Extension

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "PlantUML"
4. Install the official PlantUML extension by jebbs

### View Diagrams

1. Open any `.puml` file in VS Code
2. Click the preview button in the top right (or press `Alt+D`)
3. Diagram renders in real-time as you edit

### Export Diagrams

1. Right-click in the `.puml` file
2. Select "PlantUML: Export..."
3. Choose format: PNG, SVG, or PDF
4. Diagrams saved in same folder

---

## Option 2: Online Viewer (No Installation)

### PlantUML Online Editor

1. Visit: https://www.plantuml.com/plantuml/uml/
2. Copy-paste the contents of any `.puml` file
3. Diagram renders instantly

**Advantages:**
- No installation required
- Works on any device
- Can share links

---

## Option 3: JetBrains IDEs (IntelliJ, WebStorm, etc.)

### Built-in Support

1. Open `.puml` file in IntelliJ/WebStorm
2. Click the diagram icon in the gutter
3. Diagram preview opens in side panel

---

## Option 4: Command Line

### Install PlantUML

```bash
# Windows (via Chocolatey)
choco install plantuml

# macOS (via Homebrew)
brew install plantuml

# Or download JAR from: https://plantuml.com/download
```

### Render Diagrams

```bash
# Single diagram
plantuml modules/01_DocCheck/usecase_diagram.puml

# All diagrams in folder
plantuml modules/ -r

# Export to specific format
plantuml -tpng modules/01_DocCheck/usecase_diagram.puml
```

---

## Diagram Files by Module

### 01_DocCheck
- **usecase_diagram.puml** - Assessment tool workflow
- **class_diagram.puml** - DocCheckSession, DocCheckResult entities
- **sequence_diagram.puml** - Question flow to result

### 02_DocReady
- **usecase_diagram.puml** - Order creation workflow
- **class_diagram.puml** - FizboOrder, Payment, Property entities
- **sequence_diagram.puml** - Full checkout to account creation

### 03_Documents
- **usecase_diagram.puml** - Document lifecycle
- **class_diagram.puml** - FizboDocument, Storage entities
- **sequence_diagram.puml** - Upload to expiry monitoring

### 04_SmartCMA
- **usecase_diagram.puml** - Report generation
- **class_diagram.puml** - Report sections and data
- **sequence_diagram.puml** - Valuation to PDF generation

### 05_Operator
- **usecase_diagram.puml** - Operator dashboard features
- **class_diagram.puml** - Queue, management, coordination entities
- **sequence_diagram.puml** - Order processing workflow

### 06_Payments
- **usecase_diagram.puml** - Payment and refund flows
- **class_diagram.puml** - Payment, pricing, refund entities
- **sequence_diagram.puml** - Checkout to confirmation

---

## Quick Viewing Steps

### Step 1: Install VS Code Extension
```
1. Open VS Code
2. Ctrl+Shift+X → Search "PlantUML" → Install
3. Done!
```

### Step 2: Open a Diagram
```
1. Navigate to: c:\Users\send6\Desktop\pfe_seller_platform\modules
2. Open any folder (e.g., 01_DocCheck)
3. Open any `.puml` file
4. Right-click → "PlantUML: Open Diagram to the Side"
```

### Step 3: View & Edit
```
The diagram appears in a preview pane
Edit the .puml file and see changes in real-time
```

---

## Diagram Legend

### Use Case Diagrams
- **Actors** (stick figures): Users or external systems
- **Use Cases** (ovals): Features or actions
- **Relationships** (arrows): Who does what

### Class Diagrams
- **Classes** (boxes): Data entities
- **Properties** (list in box): Attributes
- **Methods** (list in box): Operations
- **Relationships** (lines): How entities connect
  - **→** Single connection
  - **--→** Association
  - **◇--** Aggregation

### Sequence Diagrams
- **Actors** (top left): Users and systems
- **Messages** (arrows): API calls, database queries
- **Flow** (top to bottom): Time progression
- **Alt blocks** (boxes): Conditional logic

---

## Common PlantUML Syntax

```puml
@startuml ModuleName
' This is a comment

' Use Case Diagram
usecase "Feature" as UC1
actor User
User --> UC1

' Class Diagram
class Entity {
  - property: Type
  --
  + method(): ReturnType
}

' Sequence Diagram
actor User
participant "System"
User -> System: Request
System --> User: Response

@enduml
```

---

## Rendering All Diagrams at Once

### Using VS Code Command Palette

1. Press Ctrl+Shift+P
2. Type "PlantUML: Export..."
3. Select "Export all diagrams to folder"

### Using Command Line

```bash
cd c:\Users\send6\Desktop\pfe_seller_platform\modules
plantuml **/*.puml -tpng -r
```

This generates PNG files for all diagrams.

---

## Troubleshooting

### Diagram Won't Render
- ✓ Check syntax: No unclosed brackets
- ✓ Verify @startuml and @enduml match
- ✓ Reload VS Code extension

### PlantUML Extension Not Working
- ✓ Reload VS Code (Ctrl+R)
- ✓ Reinstall extension
- ✓ Check Java is installed (required for PlantUML)

### Want to Edit Online
- Use: https://www.plantuml.com/plantuml/uml/
- Copy content → paste → edit → export

---

## Recommended Workflow

1. **For viewing**: Use VS Code with PlantUML extension
2. **For editing**: Edit `.puml` files in VS Code
3. **For exporting**: Right-click → Export to PNG/SVG
4. **For sharing**: Share PNG/SVG files or link to online editor

---

## Next Steps

1. ✅ Install PlantUML extension in VS Code
2. ✅ Open `modules/01_DocCheck/usecase_diagram.puml`
3. ✅ View the diagram in preview pane
4. ✅ Explore all 6 modules
5. ✅ Reference diagrams during development

---

## Additional Resources

- **PlantUML Official**: https://plantuml.com
- **PlantUML Syntax**: https://plantuml.com/guide
- **Online Editor**: https://www.plantuml.com/plantuml/uml/
- **VS Code Extension**: Search "PlantUML" in Extensions

---

**Happy diagramming! 📊**
