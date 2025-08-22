# System Diagrams

This document contains all system diagrams for the Sigma to RML Transpiler project, created using Mermaid.js syntax.

## UI Flow Diagram

The UI flow diagram shows the user interaction flow through the application interface.

```mermaid
flowchart TD
    A[User Opens App] --> B[Home Page]
    B --> C{User Choice}
    
    C -->|Text Input| D[Sigma to RML Page]
    C -->|File Upload| E[File Management]
    C -->|Simple Transpile| F[Transpile Page]
    
    D --> G[Enter Sigma Rule]
    G --> H[Click Translate]
    H --> I[Display RML Output]
    I --> J[Copy/Download RML]
    
    E --> K[Upload Sigma File]
    K --> L[File Listed]
    L --> M[Click Translate]
    M --> N[Generate RML File]
    N --> O[View RML Content]
    
    F --> P[Enter Simple Rule]
    P --> Q[Click Transpile]
    Q --> R[Show RML Result]
    
    J --> S[Continue with New Rule]
    O --> S
    R --> S
    S --> C
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style I fill:#e8f5e8
    style N fill:#e8f5e8
    style R fill:#e8f5e8
```

## Data Flow Diagram (DFD)

The data flow diagram illustrates how data moves through the system components.

```mermaid
flowchart TD
    A[User Input] --> B[Frontend UI]
    B --> C[HTTP Request]
    C --> D[FastAPI Backend]
    
    D --> E{Input Type}
    E -->|YAML String| F[YAML Parser]
    E -->|File Upload| G[File Handler]
    
    F --> H[Sigma Rule Dict]
    G --> I[File Storage]
    I --> H
    
    H --> J[Transpiler Engine]
    J --> K[Condition Parser]
    K --> L[AST Builder]
    
    L --> M{Pattern Type}
    M -->|Basic| N[Basic RML Generator]
    M -->|Temporal| O[Temporal RML Generator]
    M -->|Quantifier| P[Quantifier Expander]
    
    N --> Q[RML Output]
    O --> Q
    P --> Q
    
    Q --> R[Response Formatter]
    R --> S[HTTP Response]
    S --> T[Frontend Display]
    
    G --> U[File Registry]
    I --> U
    U --> V[Metadata Storage]
    
    style A fill:#e3f2fd
    style J fill:#fff3e0
    style Q fill:#e8f5e8
    style T fill:#f3e5f5
```

## UML Class Diagram - Core Transpiler Engine

The UML class diagram shows the structure and relationships of the core transpiler classes.

```mermaid
classDiagram
    class RefactoredTranspiler {
        -condition_simplifier: ConditionSimplifier
        -quantifier_expander: QuantifierExpander
        -field_extractor: FieldValueExtractor
        -rml_generator: RMLLineGenerator
        -variable_counter: int
        +transpile(sigma_rule: Union[str, Dict]) str
        -_is_temporal_condition(condition: str, detection: Dict) bool
        -_generate_basic_rml(sigma_rule: Dict, condition: str, selections: List) str
        -_generate_temporal_rml(sigma_rule: Dict, condition: str) str
        -_convert_timeframe_to_ms(timeframe: str) int
        -_generate_temporal_monitor(condition: str, selections: List, timeframe_ms: int) str
    }
    
    class ConditionSimplifier {
        <<static>>
        +simplify_condition(condition: str) str
        -_parse_condition(condition: str, last_idx: int, par_map: dict) tuple
        -_regenerate_condition(condition: str, parse_map: dict, flag: bool, operation: str, level: int) List
        -_is_selection_negated(selection_name: str, condition: str) bool
    }
    
    class QuantifierExpander {
        <<static>>
        +expand_quantifiers(condition: str, selections: List) str
        -_expand_all_of(condition: str, selections: List) str
        -_expand_any_of(condition: str, selections: List) str
        -_expand_one_of(condition: str, selections: List) str
        -_expand_n_of(condition: str, selections: List) str
    }
    
    class FieldValueExtractor {
        <<static>>
        +extract_field_values(field_data: Any, variable_counter: int) tuple
        +format_field_value(field_value: FieldValue) str
    }
    
    class RMLLineGenerator {
        <<static>>
        +generate_logsource_filter(logsource: Dict) str
        +generate_selection_definition(selection: Selection) str
        +generate_main_expression() str
        +generate_monitor_expression(condition: str, selections: List) str
    }
    
    class FieldValue {
        +field_name: str
        +value: Any
        +modifier: Optional[str]
        +variable_name: Optional[str]
    }
    
    class Selection {
        +name: str
        +fields: Dict[str, FieldValue]
        +negated: bool
    }
    
    class ConditionNode {
        +operator: str
        +left: Any
        +right: Any
        +negated: bool
    }
    
    class ConditionType {
        <<enumeration>>
        BASIC
        TEMPORAL
        QUANTIFIER
    }
    
    RefactoredTranspiler --> ConditionSimplifier : uses
    RefactoredTranspiler --> QuantifierExpander : uses
    RefactoredTranspiler --> FieldValueExtractor : uses
    RefactoredTranspiler --> RMLLineGenerator : uses
    
    FieldValueExtractor --> FieldValue : creates
    RMLLineGenerator --> Selection : uses
    Selection --> FieldValue : contains
    
    RefactoredTranspiler --> ConditionType : determines
    
    note for RefactoredTranspiler "Main transpiler class that orchestrates the conversion process"
    note for ConditionSimplifier "Applies De Morgan's laws and simplifies complex conditions"
    note for QuantifierExpander "Expands Sigma quantifier patterns to explicit conditions"
    note for FieldValueExtractor "Extracts and formats field values with modifiers"
    note for RMLLineGenerator "Generates individual RML code sections"
```

## Component Interaction Diagram

This diagram shows how the different components interact during the transpilation process.

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend API
    participant T as Transpiler
    participant S as Storage
    
    U->>F: Enter Sigma Rule
    F->>B: POST /transpile
    B->>T: transpile(sigma_rule)
    
    T->>T: Parse YAML
    T->>T: Extract Components
    T->>T: Check Temporal
    T->>T: Generate RML
    
    alt Basic Rule
        T->>T: _generate_basic_rml()
    else Temporal Rule
        T->>T: _generate_temporal_rml()
    end
    
    T->>B: Return RML String
    B->>F: HTTP Response
    F->>U: Display RML
    
    U->>F: Upload File
    F->>B: POST /upload
    B->>S: Store File
    S->>B: File Path
    B->>F: Upload Success
    
    U->>F: Translate File
    F->>B: POST /translate/{filename}
    B->>S: Read File
    S->>B: File Content
    B->>T: transpile(content)
    T->>B: RML Output
    B->>S: Save RML
    B->>F: Translation Complete
    F->>U: Show Results
```

## File Storage Architecture

This diagram illustrates the file storage and management system.

```mermaid
flowchart TD
    A[User Upload] --> B[Upload Handler]
    B --> C[File Validation]
    C --> D[File Storage]
    
    D --> E[uploaded_files/]
    D --> F[File Registry]
    
    F --> G[file_registry.json]
    G --> H[Metadata Storage]
    
    I[Translation Request] --> J[File Reader]
    J --> E
    J --> K[Transpiler]
    K --> L[RML Generator]
    
    L --> M[translated_files/]
    L --> N[Update Registry]
    N --> G
    
    O[File Management] --> P[File Lister]
    P --> G
    P --> Q[File Viewer]
    Q --> E
    Q --> M
    
    style E fill:#e8f5e8
    style M fill:#e8f5e8
    style G fill:#fff3e0
```

## Error Handling Flow

This diagram shows how errors are handled throughout the system.

```mermaid
flowchart TD
    A[Input Received] --> B[Validation Layer]
    B --> C{Valid Input?}
    
    C -->|No| D[Format Error]
    C -->|Yes| E[Processing Layer]
    
    D --> F[400 Bad Request]
    F --> G[Error Response]
    
    E --> H{Processing Success?}
    H -->|No| I[Processing Error]
    H -->|Yes| J[Success Response]
    
    I --> K[500 Internal Error]
    K --> G
    
    L[File Operations] --> M{File Exists?}
    M -->|No| N[404 Not Found]
    M -->|Yes| O[File Processing]
    
    N --> G
    O --> P{File Valid?}
    P -->|No| D
    P -->|Yes| E
    
    style D fill:#ffebee
    style I fill:#ffebee
    style N fill:#ffebee
    style J fill:#e8f5e8
```

## Performance Monitoring Flow

This diagram shows how the system monitors and reports performance metrics.

```mermaid
flowchart TD
    A[Request Start] --> B[Timer Start]
    B --> C[Input Processing]
    C --> D[Transpilation]
    D --> E[Response Generation]
    E --> F[Timer End]
    
    F --> G[Calculate Duration]
    G --> H[Log Metrics]
    H --> I[Performance Database]
    
    J[Health Check] --> K[System Status]
    K --> L[Resource Usage]
    L --> M[Response Time]
    
    M --> N[Alert System]
    N --> O{Threshold Exceeded?}
    O -->|Yes| P[Send Alert]
    O -->|No| Q[Continue Monitoring]
    
    style H fill:#e3f2fd
    style I fill:#fff3e0
    style P fill:#ffebee
```

These diagrams provide a comprehensive view of the system architecture, data flow, and component interactions. They can be rendered using any Mermaid.js compatible viewer or documentation system.
