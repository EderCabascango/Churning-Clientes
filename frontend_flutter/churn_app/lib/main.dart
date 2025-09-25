import 'package:flutter/material.dart';
import 'api_service.dart';

void main() {
  runApp(const ChurnApp());
}

class ChurnApp extends StatelessWidget {
  const ChurnApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Fuyu - Churn Prediction',
      theme: ThemeData(
        primarySwatch: Colors.indigo,
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: const PredictionScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class PredictionScreen extends StatefulWidget {
  const PredictionScreen({super.key});

  @override
  _PredictionScreenState createState() => _PredictionScreenState();
}

class _PredictionScreenState extends State<PredictionScreen> {
  final ApiService api = ApiService();
  String errorMessage = "";
  List<Map<String, dynamic>>? predictions;

  Future<void> _predictCsv() async {
    try {
      final results = await api.uploadCsvAndPredict();
      setState(() {
        predictions = results;
        errorMessage = "";
      });
    } catch (e) {
      setState(() {
        errorMessage = "Error: $e";
        predictions = null;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Image.asset("assets/fuyu_logo.png", height: 30), // logo en assets
            const SizedBox(width: 10),
            const Text("Fuyu - Churn Prediction"),
          ],
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "📌 Predicción de Fuga de Clientes",
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              "Este proyecto predice la probabilidad de que un cliente abandone "
              "un servicio de telecomunicaciones, utilizando Machine Learning. "
              "Sube un archivo CSV para obtener predicciones por lote.",
              style: TextStyle(fontSize: 15, color: Colors.black87),
            ),
            const SizedBox(height: 20),

            Center(
              child: ElevatedButton.icon(
                onPressed: _predictCsv,
                icon: const Icon(Icons.upload_file),
                label: const Text("Subir CSV y predecir"),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(
                    vertical: 12.0,
                    horizontal: 20.0,
                  ),
                ),
              ),
            ),
            const SizedBox(height: 20),

            if (errorMessage.isNotEmpty)
              Text(
                errorMessage,
                style: const TextStyle(color: Colors.red, fontSize: 16),
              ),

            if (predictions != null)
              Expanded(
                child: ListView.builder(
                  itemCount: predictions!.length,
                  itemBuilder: (context, index) {
                    final item = predictions![index];
                    final isChurn = item["prediction"] == 1;

                    return Card(
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12),
                      ),
                      elevation: 3,
                      margin: const EdgeInsets.symmetric(vertical: 6),
                      child: ListTile(
                        leading: Icon(
                          isChurn ? Icons.warning_amber : Icons.check_circle,
                          color: isChurn ? Colors.red : Colors.green,
                          size: 32,
                        ),
                        title: Text(
                          isChurn
                              ? "Cliente en riesgo de Churn"
                              : "Cliente estable",
                          style: TextStyle(
                            color: isChurn ? Colors.red : Colors.green,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        subtitle: Text(
                          "Probabilidad: ${(item["probability"] * 100).toStringAsFixed(2)}%",
                        ),
                        trailing: Text("#${item["index"]}"),
                      ),
                    );
                  },
                ),
              ),
          ],
        ),
      ),
    );
  }
}
