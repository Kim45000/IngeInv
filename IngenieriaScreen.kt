package com.example.ckmtechnologies

import android.util.Log
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Analytics
import androidx.compose.material.icons.filled.Calculate
import androidx.compose.material.icons.filled.Description
import androidx.compose.material.icons.filled.Engineering
import androidx.compose.material.icons.filled.List
import androidx.compose.material.icons.filled.Map
import androidx.compose.material.icons.filled.MyLocation
import androidx.compose.material.icons.filled.People
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.example.ckmtechnologies.network.PersonalItem

/**
 * Pantalla principal del Ingeniero.
 * Gestion completa: personal, maquinas, reportes, planos, predicciones,
 * calculadora solar y compilador LaTeX.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun IngenieriaScreen(
    personal: PersonalItem,
    serverViewModel: ServerViewModel,
    onNavigateToMaquinas: () -> Unit = {},
    onNavigateToPersonal: () -> Unit = {},
    onNavigateToProgramaciones: () -> Unit = {},
    onNavigateToSpatial: () -> Unit,
    onNavigateToPredicciones: () -> Unit = {},
    onNavigateToAssistant: () -> Unit = {},
    onNavigateToCalculator: () -> Unit,
    onNavigateToLatex: () -> Unit,
    onLogout: () -> Unit,
    onNavigateToSettings: () -> Unit,
    onNavigateToProfile: () -> Unit,
) {


    androidx.activity.compose.BackHandler(enabled = true) {}



    Scaffold(
        topBar = {
            CenterAlignedTopAppBar(
                title = { Text("Ingenieria") },
                navigationIcon = {
                    IconButton(onClick = onNavigateToSettings) {
                        Icon(Icons.Default.Settings, contentDescription = "Configuración")
                    }
                },
                actions = {
                    Text(
                        personal.nombre,
                        style = MaterialTheme.typography.labelMedium,
                        modifier = Modifier
                            .padding(end = 12.dp)
                            .clickable {
                                Log.d("IngenieriaScreen", "Profile click")
                                try {
                                    onNavigateToProfile()
                                } catch (t: Throwable) {
                                    Log.e("IngenieriaScreen", "Error navigating to profile", t)
                                }
                            }
                    )
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(24.dp)
                .verticalScroll(rememberScrollState()),
            verticalArrangement = Arrangement.spacedBy(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                "Bienvenido, ${personal.nombre}",
                style = MaterialTheme.typography.headlineSmall
            )

            Spacer(modifier = Modifier.height(8.dp))

            // --- Gestion ---
            Text("Gestion", style = MaterialTheme.typography.titleSmall,
                color = MaterialTheme.colorScheme.primary)

            ElevatedCard(onClick = onNavigateToMaquinas, modifier = Modifier.fillMaxWidth()) {
                Row(modifier = Modifier.padding(20.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Settings, null, Modifier.size(40.dp), MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.width(16.dp))
                    Column {
                        Text("Maquinas", style = MaterialTheme.typography.titleMedium)
                        Text("Gestion de equipos, estados y componentes", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }

            ElevatedCard(onClick = onNavigateToPersonal, modifier = Modifier.fillMaxWidth()) {
                Row(modifier = Modifier.padding(20.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.People, null, Modifier.size(40.dp), MaterialTheme.colorScheme.secondary)
                    Spacer(Modifier.width(16.dp))
                    Column {
                        Text("Personal", style = MaterialTheme.typography.titleMedium)
                        Text("Gestion de tecnicos y operarios", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }

            ElevatedCard(onClick = onNavigateToProgramaciones, modifier = Modifier.fillMaxWidth()) {
                Row(modifier = Modifier.padding(20.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.List, null, Modifier.size(40.dp), MaterialTheme.colorScheme.secondary)
                    Spacer(Modifier.width(16.dp))
                    Column {
                        Text("Programaciones", style = MaterialTheme.typography.titleMedium)
                        Text("Diseñar y ajustar cronogramas de mantenimiento", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }

                    ElevatedCard(onClick = onNavigateToSpatial, modifier = Modifier.fillMaxWidth()) {
                Row(modifier = Modifier.padding(20.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Map, null, Modifier.size(40.dp), MaterialTheme.colorScheme.tertiary)
                    Spacer(Modifier.width(16.dp))
                    Column {
                        Text("Planos y Datos Espaciales", style = MaterialTheme.typography.titleMedium)
                        Text(
                            "Dibuja planos, captura sensores y genera mapas espaciales",
                            style = MaterialTheme.typography.bodySmall
                        )
                    }
                }
            }

            ElevatedCard(onClick = onNavigateToPredicciones, modifier = Modifier.fillMaxWidth()) {
                Row(modifier = Modifier.padding(20.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Analytics, null, Modifier.size(40.dp), MaterialTheme.colorScheme.error)
                    Spacer(Modifier.width(16.dp))
                    Column {
                        Text("Predicciones", style = MaterialTheme.typography.titleMedium)
                        Text("Análisis predictivo de programaciones", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }

            ElevatedCard(onClick = onNavigateToAssistant, modifier = Modifier.fillMaxWidth()) {
                Row(modifier = Modifier.padding(20.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Engineering, null, Modifier.size(40.dp), MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.width(16.dp))
                    Column {
                        Text("Asistente AaaS", style = MaterialTheme.typography.titleMedium)
                        Text("Sincroniza y aplica recomendaciones en tiempo real", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }

            Divider(modifier = Modifier.padding(vertical = 4.dp))

            // --- Herramientas ---
            Text("Herramientas", style = MaterialTheme.typography.titleSmall,
                color = MaterialTheme.colorScheme.primary)

            ElevatedCard(onClick = onNavigateToCalculator, modifier = Modifier.fillMaxWidth()) {
                Row(modifier = Modifier.padding(20.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Calculate, null, Modifier.size(40.dp), MaterialTheme.colorScheme.tertiary)
                    Spacer(Modifier.width(16.dp))
                    Column {
                        Text("Calculadora Solar", style = MaterialTheme.typography.titleMedium)
                        Text("Dimensionamiento de sistemas fotovoltaicos", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }

            ElevatedCard(onClick = onNavigateToLatex, modifier = Modifier.fillMaxWidth()) {
                Row(modifier = Modifier.padding(20.dp), verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.Description, null, Modifier.size(40.dp), MaterialTheme.colorScheme.onSurfaceVariant)
                    Spacer(Modifier.width(16.dp))
                    Column {
                        Text("Compilador LaTeX", style = MaterialTheme.typography.titleMedium)
                        Text("Editor y visualizador de documentos", style = MaterialTheme.typography.bodySmall)
                    }
                }
            }

        }
    }

}
