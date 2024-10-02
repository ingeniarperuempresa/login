<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IngenIAr Registro</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
            width: 320px;
        }
        h1 {
            text-align: center;
            color: #ff6f20;
        }
        label {
            margin-top: 10px;
            display: block;
            font-weight: bold;
            color: #333;
        }
        input[type="text"], input[type="password"] {
            width: calc(100% - 22px);
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[type="button"] {
            width: 100%;
            padding: 10px;
            margin-top: 15px;
            background-color: #ff6f20;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
        }
        input[type="button"]:hover {
            background-color: #e65c00;
        }
        #message {
            text-align: center;
            margin-top: 10px;
            color: #d9534f;
        }
        /* Estilos para la barra de carga */
        #loading {
            display: none;
            text-align: center;
            margin-top: 10px;
            color: #333;
        }
        .loader {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #ff6f20;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>IngenIAr Registro</h1>
        <form id="registerForm">
            <label for="nombre">Nombre:</label>
            <input type="text" id="nombre" name="nombre" required>

            <label for="celular">Celular:</label>
            <input type="text" id="celular" name="celular" required>

            <label for="contraseña">Contraseña:</label>
            <input type="password" id="contraseña" name="contraseña" required>

            <label for="sueños">¿Qué quieres lograr?</label>
            <input type="text" id="sueños" name="sueños">

            <label for="time">¿En qué tiempo lo quieres lograr?</label>
            <input type="text" id="time" name="time">

            <label for="hechos">¿Qué has hecho hasta ahora para lograrlos?</label>
            <input type="text" id="hechos" name="hechos">

            <input type="button" value="Registrar" onclick="registerUser()">
        </form>
        <p id="message"></p>
        <div id="loading">
            <div class="loader"></div>
            <p>Cargando...</p>
        </div>
    </div>

    <script>
        function registerUser() {
            const nombre = document.getElementById('nombre').value;
            const celular = document.getElementById('celular').value;
            const contraseña = document.getElementById('contraseña').value;
            const sueños = document.getElementById('sueños').value;
            const time = document.getElementById('time').value;
            const hechos = document.getElementById('hechos').value;

            // Mostrar la barra de carga
            document.getElementById('loading').style.display = 'block';

            google.script.run.withSuccessHandler(function(success) {
                const message = document.getElementById('message');
                // Ocultar la barra de carga
                document.getElementById('loading').style.display = 'none';

                if (success) {
                    message.innerText = 'Registro exitoso!';
                    message.style.color = '#5cb85c'; // Color de éxito
                    document.getElementById('registerForm').reset(); // Limpiar el formulario
                    // Redirigir a la página de destino
                    window.location.href = 'https://panelingeniarperu.streamlit.app';
                } else {
                    message.innerText = 'Error en el registro.';
                    message.style.color = '#d9534f'; // Color de error
                }
            }).registerUser(nombre, celular, contraseña, sueños, time, hechos);
        }
    </script>
</body>
</html>

