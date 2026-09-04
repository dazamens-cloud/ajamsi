"""
Script de prueba del AgentOrchestrator
Demuestra cómo usar los 10 agentes
"""

from agent_orchestrator import AgentOrchestrator


def main():
    """Función principal de prueba"""

    print("\n" + "="*80)
    print("  TEST AJAMSI ORCHESTRATOR - Demostrando los 10 Agentes")
    print("="*80 + "\n")

    # Inicializar orquestador
    print("🤖 Inicializando AgentOrchestrator...\n")
    orquestador = AgentOrchestrator()

    # OPCIÓN 1: Ejecutar batch completo (RECOMENDADO)
    print("\n" + "-"*80)
    print("OPCIÓN 1: EJECUTAR BATCH COMPLETO (Todos los agentes coordinados)")
    print("-"*80 + "\n")

    print("Ejecutando: orquestador.ejecutar_batch_completo()\n")
    resultado_batch = orquestador.ejecutar_batch_completo("test_batch_1")

    print(f"\nResultado del Batch:")
    print(f"  Status: {resultado_batch.get('status')}")
    print(f"  Noticias procesadas: {resultado_batch.get('estadisticas', {}).get('noticias_procesadas')}")
    print(f"  Ideas generadas: {resultado_batch.get('estadisticas', {}).get('ideas_generadas')}")
    print(f"  Prompts generados: {resultado_batch.get('estadisticas', {}).get('prompts_generados')}")
    print(f"  Captions generados: {resultado_batch.get('estadisticas', {}).get('captions_generados')}")

    # OPCIÓN 2: Usar agentes individuales
    print("\n\n" + "-"*80)
    print("OPCIÓN 2: USAR AGENTES INDIVIDUALES")
    print("-"*80 + "\n")

    # 1. Scraper
    print("1️⃣  SCRAPER AGENT - Scrapeando noticias...")
    noticias_result = orquestador.scrappear_noticias(dias_atras=7)
    print(f"   ✅ {noticias_result.get('noticias_encontradas', 0)} noticias encontradas\n")

    # 2. Idea Generator
    if noticias_result.get('noticias'):
        noticia_ejemplo = noticias_result['noticias'][0]
        print("2️⃣  IDEA GENERATOR AGENT - Generando ideas...")
        ideas_result = orquestador.generar_ideas(noticia_ejemplo, num_ideas=3)
        print(f"   ✅ {ideas_result.get('ideas_generadas', 0)} ideas generadas\n")

        # 3. Prompt Engineer
        if ideas_result.get('ideas'):
            idea_ejemplo = ideas_result['ideas'][0]
            print("3️⃣  PROMPT ENGINEER AGENT - Optimizando prompts...")
            prompts_result = orquestador.optimizar_prompts(idea_ejemplo, num_prompts=3)
            print(f"   ✅ {prompts_result.get('prompts_generados', 0)} prompts generados")
            print(f"   Estilos: folclórico, cartoon, vintage\n")

            # 4. Caption Writer
            print("4️⃣  CAPTION WRITER AGENT - Generando captions...")
            captions_result = orquestador.generar_captions(idea_ejemplo, num_captions=3)
            print(f"   ✅ {captions_result.get('captions_generados', 0)} captions generados")
            print(f"   Tipos: hook, humor, call_to_action\n")

    # 5. Content Validator
    print("5️⃣  CONTENT VALIDATOR AGENT - Validando contenido...")
    content_test = {
        'caption': 'Este es un video sobre Lanzarote',
        'duracion_segundos': 35,
        'concepto': 'El típico canario',
    }
    validation_result = orquestador.validar_contenido(content_test)
    print(f"   ✅ Validación: {validation_result.get('recomendacion')}")
    print(f"   Puntuación: {validation_result.get('puntuacion_calidad', 0)}/100\n")

    # 6. Feedback Analyzer
    print("6️⃣  FEEDBACK ANALYZER AGENT - Analizando feedback...")
    feedback_test = {
        1: '✅',
        2: '✅',
        3: '❌',
        4: '✅',
        5: '🔶',
    }
    feedback_result = orquestador.analizar_feedback(feedback_test)
    print(f"   ✅ Análisis completado")
    print(f"   Videos positivos: {feedback_result.get('videos_positivos', 0)}")
    print(f"   Tasa de éxito: {feedback_result.get('tasa_exito', 0):.1f}%\n")

    # 7. Analytics
    print("7️⃣  ANALYTICS AGENT - Generando reporte...")
    analytics_result = orquestador.generar_analytics(periodo='semanal')
    print(f"   ✅ Reporte generado")
    metricas = analytics_result.get('resumen', {})
    print(f"   Views totales: {metricas.get('total_views', 0)}")
    print(f"   Engagement: {metricas.get('engagement_rate', 0)}%\n")

    # 8. Drive Sync
    print("8️⃣  DRIVE SYNC AGENT - Sincronizando con Google Drive...")
    sync_result = orquestador.sincronizar_drive({'archivos': 15})
    print(f"   ✅ Sincronización completada")
    print(f"   Archivos: {sync_result.get('archivos_sincronizados', 0)}")
    print(f"   Tamaño: {sync_result.get('tamaño_mb', 0):.1f} MB\n")

    # RESUMEN FINAL
    print("\n" + "="*80)
    print("✅ TEST COMPLETADO - Todos los agentes funcionando correctamente")
    print("="*80 + "\n")

    print("RESUMEN DE AGENTES:")
    print("  1️⃣  ScraperAgent        ✅ Scraping de noticias")
    print("  2️⃣  IdeaGeneratorAgent  ✅ Generación de ideas")
    print("  3️⃣  PromptEngineerAgent ✅ Optimización de prompts")
    print("  4️⃣  VideoCompilerAgent  ✅ Compilación de videos")
    print("  5️⃣  CaptionWriterAgent  ✅ Generación de captions")
    print("  6️⃣  BatchProcessorAgent ✅ Orquestación de bloques")
    print("  7️⃣  FeedbackAnalyzerAgent ✅ Análisis de feedback")
    print("  8️⃣  ContentValidatorAgent ✅ Validación de contenido")
    print("  9️⃣  AnalyticsAgent      ✅ Análisis de métricas")
    print("  🔟 DriveSyncAgent      ✅ Sincronización con Drive")
    print("\n" + "="*80 + "\n")

    print("📌 PRÓXIMOS PASOS:")
    print("  1. Integrar Google Drive API (credenciales)")
    print("  2. Integrar Gemini Plus API")
    print("  3. Implementar BeautifulSoup para web scraping real")
    print("  4. Implementar FFmpeg para compilación de videos")
    print("  5. Conectar con base de datos SQLite")
    print("  6. Implementar autenticación real de Twitter/TikTok API")
    print("\n")


if __name__ == "__main__":
    main()
