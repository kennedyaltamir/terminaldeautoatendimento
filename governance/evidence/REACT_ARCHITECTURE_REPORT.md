# 🕵️ React Architecture Audit Report

**Files Scanned:** 143
**Critical Issues:** 12
**Warnings:** 3

## 🚨 Detected Issues

### 🔴 REACT_EFFECT_LOOP
- **File:** `frontend\src\app\admin\[slug]\driver\page.tsx`
- **Details:** Loop potencial: 'setActiveDeliveryId' chamado em useEffect que depende de 'activeDeliveryId'.

### 🟡 STATE_AUTHORITY_CONFLICT
- **File:** `frontend\src\app\admin\[slug]\driver\page.tsx`
- **Details:** Polling e WebSocket detectados no mesmo componente. Risco de Race Condition na atualização de estado.

### 🔴 REACT_EFFECT_LOOP
- **File:** `frontend\src\components\kiosk\KioskFullscreenToggle.tsx`
- **Details:** Loop potencial: 'setSequence' chamado em useEffect que depende de 'sequence'.

### 🔴 REACT_EFFECT_LOOP
- **File:** `frontend\src\components\kiosk\KioskFullscreenToggle.tsx`
- **Details:** Loop potencial: 'setSequence' chamado em useEffect que depende de 'sequence'.

### 🔴 REACT_EFFECT_LOOP
- **File:** `frontend\src\components\kiosk\KioskFullscreenToggle.tsx`
- **Details:** Loop potencial: 'setSequence' chamado em useEffect que depende de 'sequence'.

### 🔴 REACT_EFFECT_LOOP
- **File:** `frontend\src\components\kiosk\KioskStealthTrigger.tsx`
- **Details:** Loop potencial: 'setSequence' chamado em useEffect que depende de 'sequence'.

### 🔴 REACT_EFFECT_LOOP
- **File:** `frontend\src\components\kiosk\KioskStealthTrigger.tsx`
- **Details:** Loop potencial: 'setSequence' chamado em useEffect que depende de 'sequence'.

### 🔴 REACT_EFFECT_LOOP
- **File:** `frontend\src\components\kiosk\KioskStealthTrigger.tsx`
- **Details:** Loop potencial: 'setSequence' chamado em useEffect que depende de 'sequence'.

### 🔴 REACT_EFFECT_LOOP
- **File:** `frontend\src\components\landing\FloatingWidget.tsx`
- **Details:** Loop potencial: 'setHasShownExit' chamado em useEffect que depende de 'hasShownExit'.

### 🟡 STATE_AUTHORITY_CONFLICT
- **File:** `frontend\src\components\menu\PublicMonitorView.tsx`
- **Details:** Polling e WebSocket detectados no mesmo componente. Risco de Race Condition na atualização de estado.

### 🔴 REACT_EFFECT_LOOP
- **File:** `frontend\src\components\ui\Typewriter.tsx`
- **Details:** Loop potencial: 'setReverse' chamado em useEffect que depende de 'reverse'.

### 🔴 REACT_EFFECT_LOOP
- **File:** `frontend\src\components\ui\Typewriter.tsx`
- **Details:** Loop potencial: 'setReverse' chamado em useEffect que depende de 'reverse'.

### 🔴 REACT_EFFECT_LOOP
- **File:** `frontend\src\components\ui\Typewriter.tsx`
- **Details:** Loop potencial: 'setIndex' chamado em useEffect que depende de 'index'.

### 🔴 REACT_EFFECT_LOOP
- **File:** `frontend\src\components\ui\Typewriter.tsx`
- **Details:** Loop potencial: 'setSubIndex' chamado em useEffect que depende de 'subIndex'.

### 🟡 FLAKY_TEST_PATTERN
- **File:** `frontend\tests\kiosk_lock.spec.ts`
- **Details:** Uso de 'page.reload()' detectado. Isso limpa o estado da aplicação e pode causar falhas em testes de SPA.

