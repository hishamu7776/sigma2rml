# Sigma to RML Translation Examples

This document provides a series of examples demonstrating the translation of Sigma rules into their corresponding RML (Runtime Verification Language) properties.

---

## Example 1: Basic Selection

#### Sigma Rule
```yaml
logsource:
   product: windows
   service: application
detection:
   selection:
       EventID: 524
   condition: selection
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'application'};

// event type section
safe_selection not matches {eventid: 524};

// property section
Main = logsource >> Monitor;
Monitor = safe_selection*;
```

---

## Example 2: Selection with Multiple Fields

#### Sigma Rule
```yaml
logsource:
   product: windows
   service: application
detection:
   selection:
       EventID: 524
       Provider_Name: Microsoft-Windows-Backup
   condition: selection
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'application'};

// event type section
safe_selection not matches {eventid: 524, provider_name: 'Microsoft-Windows-Backup'};

// property section
Main = logsource >> Monitor;
Monitor = safe_selection*;
```

---

## Example 3: Selection with List of Values

#### Sigma Rule
```yaml
logsource:
   product: windows
   service: security
detection: 
   selection:
       EventID:
           - 4728
           - 4729
           - 4730
   condition: selection
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'security'};

// event type section
safe_selection not matches {eventid: 4728 | 4729 | 4730};

// property section
Main = logsource >> Monitor;
Monitor = safe_selection*;
```

---

## Example 4: `NOT` Condition

#### Sigma Rule
```yaml
logsource:
   product: windows
   service: application
detection:
   selection:
       EventID:
           - 4728
           - 4729
           - 4730
       Provider_Name: Microsoft-Windows-Backup
   condition: not selection
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup'};

// property section
Main = logsource >> Monitor;
Monitor = safe_selection*;
```

---

## Example 5: `AND` Condition

#### Sigma Rule
```yaml
logsource:
   product: windows
   service: application
detection:
   selection_1:
       EventID: 4663
   selection_2:
       ObjectName: '\Device\CdRom0\setup.exe'
   condition: selection_1 and selection_2
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection_1 not matches {eventid: 4663};
safe_selection_2 not matches {objectname: '\Device\CdRom0\setup.exe'};

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection_1 \/ safe_selection_2)*;
```

---

## Example 6: `OR` Condition

#### Sigma Rule
```yaml
logsource:
   product: windows
   service: application
detection:
   selection_1:
       EventID:
           - 4728
           - 4729
           - 4730
       Provider_Name: Microsoft-Windows-Backup
   selection_2:
       ObjectName: '\Device\CdRom0\setup.exe'
       FieldName: 'ProcessName'
   condition: selection_1 or selection_2
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection_1 not matches {eventid: 4728 | 4729 | 4730, provider_name: 'Microsoft-Windows-Backup'};
safe_selection_2 not matches {objectname: '\Device\CdRom0\setup.exe', fieldname: 'ProcessName'};

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection_1 /\ safe_selection_2)*;
```

---

## Example 7: Field with Modifier (`gte`)

#### Sigma Rule
```yaml
logsource:
   product: windows
   service: application
detection:
   selection_1:
       EventID:
           - 4728
           - 4729
       Provider_Name: Microsoft-Windows-Backup
       ObjectNumber|gte: 25
   selection_2:
       ObjectName: '\Device\CdRom0\setup.exe'
       FieldName: 'ProcessName'
   condition: selection_1 or not selection_2
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection_1 not matches {eventid: 4728 | 4729 , provider_name: 'Microsoft-Windows-Backup', objectnumber: x1} with x1 >= 25;
safe_selection_2 matches {objectname: '\Device\CdRom0\setup.exe', fieldname: 'ProcessName'};

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection_1 /\ safe_selection_2)*;
```

---

## Example 8: Grouped Conditions

#### Sigma Rule
```yaml
logsource:
   product: windows
   service: application
detection:
   selection1:
       EventID: 4663
   selection2:
       EventName: 'ProcessName'
   selection3:
       FieldName: 'something'       
   condition: selection1 and (selection2 or selection3)
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection1 not matches {eventid: 4663};
safe_selection2 not matches {eventname: 'ProcessName'};
safe_selection3 not matches {fieldname: 'something'};

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection_1 \/ Selection2)*;
Selection2 = (safe_selection2 /\ safe_selection3);
```

---

## Example 9: `all of selection*`

#### Sigma Rule
```yaml
logsource:
   product: windows
   service: application
detection:
   selection1:
       EventID: 4663
   selection2:
       EventName: 'ProcessName'
   selection3:
       FieldName: 'something'       
   condition: all of selection*
# This condition simplifies to 'selection1 and selection2 and selection3'
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection1 not matches {eventid: 4663};
safe_selection2 not matches {eventname: 'ProcessName'};
safe_selection3 not matches {fieldname: 'something'};

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection_1 \/ safe_selection2 \/ safe_selection3)*;
```

---

## Example 10: `1 of selection*`

#### Sigma Rule
```yaml
logsource:
   product: windows
   service: application
detection:
   selection1:
       EventID: 4663
       ObjectNumber|lte: 100
       ObjectValue|lt:23;
   selection2:
       FieldName: 'ProcessName'
       FieldValue|gt: 1000;
   condition: 1 of selection*
# This condition simplifies to 'selection1 or selection2'
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'application'};

// event types
safe_selection1 not matches {eventid: 4663, objectnumber: x1, objectvalue: x2} with x1 <= 100 && x2 < 23;
safe_selection2 not matches {fieldname: 'ProcessName', fieldvalue: x1} with x1 > 1000;

// property section
Main = logsource >> Monitor;
Monitor = (safe_selection1 /\ safe_selection2)*;
```

---

## Example 11: Temporal Condition with `timeframe`

#### Sigma Rule
```yaml
logsource:
    product: windows
    service: security
detection:
    selection_task:
        EventID: 4698
    selection_firewall:
        EventID: 4946
    timeframe: 5m
    condition: selection_task and selection_firewall
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'security'};

// event types
timed_selection_task(ts) matches {timestamp: ts, eventid: 4698};
timed_selection_firewall(ts) matches {timestamp: ts, eventid: 4946};
timed_other_events(ts) matches {timestamp: ts};

// property section
Main = logsource >> Monitor<0, 0, 0>!;
Monitor<start_ts, s1, s2> = 
{
    let ts; timed_selection_task(ts) (
        if (start_ts == 0 || ts - start_ts > 300000)
            Monitor<ts, 1, 0>
        else (
            if (s2 == 1) empty else Monitor<start_ts, 1, s2>
        )
    )
}
\/
{
    let ts; timed_selection_firewall(ts) (
        if (start_ts == 0 || ts - start_ts > 300000)
            Monitor<ts, 0, 1>
        else (
            if (s1 == 1) empty else Monitor<start_ts, s1, 1>                    
        )
    )
}
\/
{
    let ts; timed_other_events(ts) (
        if (start_ts > 0 && ts - start_ts > 300000)
            Monitor<0, 0, 0>            
        else (
            Monitor<start_ts, s1, s2>
        )
    )
};
```

---

## Example 12: Temporal Condition with `near`

#### Sigma Rule
```yaml
logsource:
    product: windows
    service: security
detection:
    selection_task:
        EventID: 4698
    selection_firewall:
        EventID: 4946
    condition: selection_task | near selection_firewall
# 'near' implies 'and' with a default timeframe of 10s.
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'security'};

// event types
timed_selection_task(ts) matches {timestamp: ts, eventid: 4698};
timed_selection_firewall(ts) matches {timestamp: ts, eventid: 4946};
other_events(ts) matches {timestamp: ts};

// property section
Main = logsource >> Monitor<0, 0, 0>!;
Monitor<start_ts, s1, s2> = 
{
    let ts; timed_selection_task(ts) (
        if (start_ts == 0 || ts - start_ts > 10000)
            Monitor<ts, 1, 0>
        else (
            if (s2 == 1) empty else Monitor<start_ts, 1, s2>
        )
    )
}
\/
{
    let ts; timed_selection_firewall(ts) (
        if (start_ts == 0 || ts - start_ts > 10000)
            Monitor<ts, 0, 1>
        else (
            if (s1 == 1) empty else Monitor<start_ts, s1, 1>                    
        )
    )
}
\/
{
    let ts; timed_other_events(ts) (
        if (start_ts > 0 && ts - start_ts > 10000)
            Monitor<0, 0, 0>            
        else (
            Monitor<start_ts, s1, s2>
        )
    )
};
```

---

## Example 13: Temporal Condition with `count()`

#### Sigma Rule
```yaml
logsource:
    product: windows
    service: security
detection:
    selection:
        EventID: 4663
        Accesses: 'DELETE'
    condition: selection | count() > 5
# `count()` implies a temporal condition with a default timeframe of 10s.
```

#### RML Translation
```js
// log source filter
logsource matches {product: 'windows', service: 'security'};

// event types
timed_selection(ts) matches {timestamp: ts, eventid: 4663, accesses: 'DELETE'};
safe_selection not matches {eventid: 4663, accesses: 'DELETE'};
timed_other_events(ts) matches {timestamp: ts};

// property section
Main = logsource >> Monitor<0, 0>!;
Monitor<start_ts, count> =
    {let ts; timed_selection(ts)
        (
            if (start_ts == 0 || ts - start_ts > 10000) (
                Monitor<ts, 1>
            )                
            else if (count+1 > 4) safe_selection else Monitor<start_ts,count+1>
        )
    }
    \/
    {let ts; timed_other_events(ts)
        (
            if (start_ts > 0 && ts - start_ts > 10000)
                Monitor<0, 0> 
            else
                Monitor<count, start_ts>
        )
    };
