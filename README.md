## 🧘‍♂️ Meditador de Bolsillo - Heartenic
# Diseño CAD

Este repositorio contiene el diseño paramétrico en CADQuery de la carcaza del Meditador de Bolsillo: un dispositivo portátil minimalista que guía ejercicios de respiración y meditación.
El modelo está optimizado para impresión 3D, con una forma ergonómica y compacta, pensada para acompañarte en cualquier momento y lugar.

---

## ✨ Características del Diseño

Carcaza diseñada en **CADQuery (Python)** con parámetros editables.
Optimizada **para impresión en FDM** (impresión 3D) con mínima necesidad de soportes.
Diseño ergonómico: bordes suaves y dimensiones compactas.

---

## ⚙️ Soporte interno para dos configuraciones:

### ESP32-C6 con BMS integrado:
 - ESP32-C6 Supermini.
 - BMS: Integrado (ESP32-C6)
 - Pantalla OLED 0.96" 128x64 SSD1306.
 - Motor de vibración.
 - Controlador del motor.
 - Batería LiPo (300–700 mAh).
 - Botón de 12x12 mm

### ESP32-C3 con TP4056:
 - ESP32-C3 Supermini.
 - BMS: TP4056
 - Pantalla OLED 0.96" 128x64 SSD1306.
 - Motor de vibración.
 - Controlador del motor.
 - Batería LiPo (150–300 mAh).
 - Botón de 12x12 mm
 - Variante opcional con switch físico de apagado.

 ---

 🔗 Relación con el Proyecto

Este diseño CAD es parte del meditador de bolsillo de Heartenic, junto con:
 - Firmware (Arduino/ESP32): https://github.com/Heartenic/Meditador-Arduino
 - Documentación del Proyecto: https://heartenic.com/meditador.html
