# Configuración del Webhook n8n para GICA Generador

## Respond to Webhook - Opción recomendada

En el nodo **Respond to Webhook**, use la opción **JSON**.

### Configuración

1. **Respond** → Seleccione **JSON**
2. **JSON Body** → Pegue este contenido:

```json
{
  "success": true,
  "message": "Envío aceptado. La solicitud fue recibida correctamente."
}
```

### Otras opciones (alternativas)

| Opción | Uso |
|--------|-----|
| **JSON** | **Recomendado** – Permite definir el mensaje exacto. GICA mostrará `message` al usuario. |
| First Incoming Item | Devuelve el primer item procesado por el workflow (si el formato coincide con `{success, message}`) |
| No Data | Responde vacío (200 OK). GICA mostrará mensaje genérico "Envío aceptado". |

### Flujo en n8n

1. **Webhook** – Recibe POST con `contexto`, `prompt`, `variables`
2. **Procesamiento** – Nodos de IA, transformación, etc.
3. **Respond to Webhook** (JSON) – Responde con `{"success": true, "message": "..."}`

### Mensaje en GICA

Cuando n8n responde con `message` en el JSON, GICA Generador mostrará ese texto al usuario. Si no hay `message`, se usa el mensaje predeterminado "Envío aceptado".
