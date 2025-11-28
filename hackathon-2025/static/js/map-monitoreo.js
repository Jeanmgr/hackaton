document.addEventListener("DOMContentLoaded", function () {

  // Crear mapa
  var map = L.map('map').setView([20.13528, -98.38056], 17);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 25,
    attribution: '© OpenStreetMap'
  }).addTo(map);

  // Polígono campus (solo borde)
  var campusGeoJSON = {
    "type": "FeatureCollection",
    "features": [{
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
          [-98.37790036281253, 20.1348249470946],
          [-98.37848400425189, 20.135509459859847],
          [-98.37896490857344, 20.1360746356101],
          [-98.37960913759281, 20.136827240115963],
          [-98.37972147267915, 20.136961135975127],
          [-98.38013469401342, 20.137745486286576],
          [-98.38028331503358, 20.13803249490263],
          [-98.38146018063655, 20.13700188283778],
          [-98.38224071036956, 20.13632166912626],
          [-98.38313967910035, 20.135536858035366],
          [-98.38415057278864, 20.134652713759266],
          [-98.38523132307598, 20.133710551463466],
          [-98.38452794489345, 20.13298231683393],
          [-98.3841424449794, 20.132578322019327],
          [-98.38352841982477, 20.132828778753435],
          [-98.38236865930737, 20.133297137835555],
          [-98.38158022907716, 20.13362528292383],
          [-98.38118419612066, 20.13378890057554],
          [-98.3802476898567, 20.13402475233167],
          [-98.37790036281253, 20.1348249470946]
        ]]
      }
    }]
  };

  var layer = L.geoJSON(campusGeoJSON, {
    style: {
      color: "#000000",
      weight: 3,
      fill: false,
      fillOpacity: 0
    }
  }).addTo(map);

  map.fitBounds(layer.getBounds());

  // ICONOS DE BOTE SEGÚN NIVEL DE LLENADO
  function getBoteIcon(estado) {
    // Normalizar estado a mayúsculas para comparación
    const estadoNorm = (estado || '').toUpperCase();
    
    let color = '#28a745'; // Verde por defecto (vacío)
    
    if (estadoNorm === 'LLENO' || estadoNorm.includes('LLENO') || estadoNorm === 'FULL') {
      color = '#dc3545'; // Rojo - LLENO
    } else if (estadoNorm === 'MEDIO' || estadoNorm.includes('MEDIO') || estadoNorm === 'MEDIUM' || estadoNorm === 'HALF') {
      color = '#ffc107'; // Amarillo - MEDIO
    } else if (estadoNorm === 'VACIO' || estadoNorm.includes('VACIO') || estadoNorm === 'EMPTY' || estadoNorm === 'VACÍO') {
      color = '#28a745'; // Verde - VACÍO
    }
    
    console.log(`Sensor estado: "${estado}" → Color: ${color}`);
    
    // Crear ícono SVG en línea con el color correspondiente
    const svgIcon = `
      <svg width="40" height="40" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
        <path fill="${color}" stroke="#000" stroke-width="0.5" d="M6 2L3 6v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V6l-3-4H6zm0 2h12l2 3v13H4V7l2-3zm2 5v8h8v-8H8z"/>
      </svg>
    `;
    
    return L.divIcon({
      html: svgIcon,
      iconSize: [40, 40],
      iconAnchor: [20, 40],
      popupAnchor: [0, -32],
      className: 'custom-marker-icon'
    });
  }
  
  // Añadir estilos para los iconos personalizados
  const style = document.createElement('style');
  style.textContent = `
    .custom-marker-icon {
      background: none !important;
      border: none !important;
    }
  `;
  document.head.appendChild(style);

  // Coordenadas de botes (predefinidas como fallback)
  const coordenadasPorDefecto = [
    [20.136166, -98.381506],
    [20.134718, -98.382346],
    [20.134887, -98.381758],
    [20.135258, -98.381348],
    [20.135343, -98.381040],
    [20.135071, -98.380557],
    [20.135549, -98.379422],
    [20.134957, -98.379366]
  ];

  // Cargar sensores desde Firebase
  async function cargarSensores() {
    try {
      const response = await fetch("/api/sensores/");
      const sensores = await response.json();

      if (sensores && typeof sensores === 'object') {
        let index = 0;
        for (const [sensorId, sensorData] of Object.entries(sensores)) {
          // Usar coordenadas predefinidas o las del sensor si existen
          const coords = coordenadasPorDefecto[index] || coordenadasPorDefecto[0];
          
          // Determinar el ícono según el estado del contenedor
          const estado = sensorData.estado_contenedor || 'VACIO';
          const marker = L.marker(coords, { icon: getBoteIcon(estado) }).addTo(map);

          // Crear popup con información del sensor
          const popupContent = `
            <div style="min-width: 200px;">
              <h3 style="margin: 0 0 10px 0;">🗑️ Contenedor #${sensorId}</h3>
              <p style="margin: 5px 0;"><strong>Estado:</strong> ${sensorData.estado_contenedor || 'Desconocido'}</p>
              <p style="margin: 5px 0;"><strong>Distancia:</strong> ${sensorData.distancia_cm || 'N/A'} cm</p>
              <p style="margin: 5px 0;"><strong>Luminosidad:</strong> ${sensorData.luminosidad || 'N/A'}</p>
              <p style="margin: 5px 0;"><strong>Toxicidad:</strong> ${sensorData.toxicidad || 'N/A'}</p>
            </div>
          `;
          
          marker.bindPopup(popupContent);

          marker.on("click", () => {
            map.flyTo(coords, 20, { animate: true, duration: 1.0 });
            marker.openPopup();
          });

          index++;
        }
      } else {
        // Si no hay sensores en Firebase, usar coordenadas por defecto
        console.log("No hay sensores en Firebase, mostrando ubicaciones por defecto");
        mostrarMarcadoresPorDefecto();
      }
    } catch (error) {
      console.error("Error al cargar sensores:", error);
      mostrarMarcadoresPorDefecto();
    }
  }

  // Función para mostrar marcadores por defecto si no hay sensores
  function mostrarMarcadoresPorDefecto() {
    coordenadasPorDefecto.forEach((coords, i) => {
      const marker = L.marker(coords, { icon: getBoteIcon('VACIO') }).addTo(map);
      marker.bindPopup("🗑️ Contenedor #" + (i + 1));
      marker.on("click", () => {
        map.flyTo(coords, 20, { animate: true, duration: 1.0 });
        marker.openPopup();
      });
    });
  }

  // Cargar sensores al iniciar
  cargarSensores();

  // Botón de reset
  const resetBtn = document.getElementById("resetMap");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      map.flyTo([20.13528, -98.38056], 17, { animate: true, duration: 1.0 });
    });
  }

});