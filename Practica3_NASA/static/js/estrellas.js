// Obtener el canvas
const canvas = document.getElementById('canvas-estrellas');

// Verificar que el canvas existe
if (canvas) {
    const ctx = canvas.getContext('2d');
    
    // Función para ajustar tamaño
    function ajustarTamanio() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    // Ajustar tamaño inicial y al cambiar ventana
    ajustarTamanio();
    window.addEventListener('resize', ajustarTamanio);
    
    // Crear array de estrellas
    let estrellas = [];
    
    // Generar 200 estrellas
    for (let i = 0; i < 200; i++) {
        estrellas.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            size: Math.random() * 2,
            brillo: Math.random() * 0.05,
            fase: Math.random() * Math.PI * 2
        });
    }
    
    // Función de animación
    function animar() {
        // Limpiar canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Dibujar cada estrella
        estrellas.forEach(function(estrella) {
            // Actualizar fase para el parpadeo
            estrella.fase += estrella.brillo;
            
            // Calcular opacidad (entre 0 y 1)
            let opacidad = (Math.sin(estrella.fase) + 1) / 2;
            
            // Configurar color con opacidad
            ctx.fillStyle = 'rgba(255, 255, 255, ' + opacidad + ')';
            
            // Dibujar círculo (estrella)
            ctx.beginPath();
            ctx.arc(estrella.x, estrella.y, estrella.size, 0, Math.PI * 2);
            ctx.fill();
        });
        
        // Solicitar siguiente frame
        requestAnimationFrame(animar);
    }
    
    // Iniciar animación
    animar();
}