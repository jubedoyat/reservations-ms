# Microservicio _reservations-ms_

Este microservicio gestiona las reservas hechas por los usuarios para vuelos específicos.

> **Importante:** Los microservicios `users-ms` y `flights-ms` deben estar en ejecución antes de utilizar los endpoints de este microservicio. También vale la pena aclarar que para utilizar estos endpoints es necesario haber antes obtenido un token de acceso en el microservicio de users-ms por medio del endpoint de `/login` y usarlo en `/docs` y usarlo en la parte superior derecha.

## Funcionalidades principales

* Crear nuevas reservas.
* Consultar reservas hechas por el usuario autenticado.
* Eliminar y actualizar reservas existentes.

## Instrucciones de Uso

1. Clonar el repositorio:

```
git clone https://github.com/jubedoyat/reservations-ms.git
```

2. Abrir el proyecto desde VSCode o terminal.

3. (Opcional) Crear y activar un entorno virtual:

```
python -m venv venv
source venv/bin/activate
```

4. Instalar dependencias:

```
pip install -r requirements.txt
```

5. Ejecutar el microservicio:

```
uvicorn app.main:app --reload --port 8002
```

6. Acceder desde el navegador:

```
http://127.0.0.1:8002
```

## Endpoints

- `POST /reservations/`: crea una nueva reserva (requiere token JWT).
- `GET /reservations/`: obtiene todas las reservas del usuario autenticado.
- `DELETE /reservations/{reservation_id}`: elimina una reserva si pertenece al usuario autenticado.
- `PUT /reservations/{reservation_id}`: actualiza una reserva si pertenece al usuario autenticado.
- `GET /reservations/{reservation_id}`: obtiene una reserva por ID.

### Uso

Usar `/docs/` para interactuar. Es necesario autenticarse primero con el token JWT obtenido desde `users-ms` (`/login`).

### Parámetros

- `reservation_id`: Identificador único de la reserva en la base de datos MongoDB. Este valor se utiliza en los endpoints `GET /reservations/{reservation_id}`, `PUT /reservations/{reservation_id}` y `DELETE /reservations/{reservation_id}` para consultar, actualizar o eliminar una reserva específica.

- En la creación de una reserva (`POST /reservations/`), el cuerpo de la solicitud debe incluir:
  * `flight_id`: ID del vuelo al que se desea asociar la reserva (debe existir en el microservicio `flights-ms`).
  * `seat`: Asiento reservado (ej. `"30A"`).
  * `boarding_time`: Fecha y hora de abordaje, en formato ISO 8601 (ej. `"2025-04-27T22:30:00"`).
  * `luggage`: Objeto con los campos `hold_bags` (equipaje en bodega) y `hand_bags` (equipaje de mano), ambos como números enteros.
  * `pets` *(opcional)*: Lista de objetos que describen mascotas, donde cada uno tiene `species` (ej. `"dog"`) y `hold` (booleano que indica si viaja en bodega).

> Todos los endpoints protegidos requieren que el usuario esté autenticado y envíe su token JWT en la cabecera `Authorization` con el formato `Bearer <token>`.

---

### Resultados

- `POST /reservations/`: Devuelve el objeto completo de la reserva creada si los datos son válidos y el usuario está autenticado. Valida internamente que el `user_id` (extraído del token) y el `flight_id` existan en los microservicios correspondientes.

- `GET /reservations/`: Retorna una lista de todas las reservas asociadas al usuario autenticado. Si no existen reservas, devuelve una lista vacía. Este endpoint garantiza que los usuarios solo puedan acceder a sus propias reservas.

- `GET /reservations/{reservation_id}`: Devuelve la reserva correspondiente al ID indicado **solo si pertenece al usuario autenticado**. En caso contrario, se devuelve un error `403 Forbidden` o `404 Not Found`.

- `PUT /reservations/{reservation_id}`: Actualiza la reserva con los nuevos datos proporcionados en el cuerpo de la solicitud, y devuelve el objeto actualizado. Solo puede ser usada por el dueño de la reserva.

- `DELETE /reservations/{reservation_id}`: Elimina la reserva indicada si pertenece al usuario. Devuelve un mensaje de éxito en caso de eliminación correcta.

- En todos los casos, si el token JWT es inválido, expirado o no se proporciona, se devuelve un error `401 Unauthorized`. Si el usuario intenta manipular una reserva que no le pertenece, se devuelve `403 Forbidden`. Si el recurso no existe, se devuelve `404 Not Found`.
