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
      title: 'Churn Prediction',
      theme: ThemeData(primarySwatch: Colors.indigo),
      home: const PredictionScreen(),
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
      appBar: AppBar(title: const Text("Churn Prediction")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            ElevatedButton(
              onPressed: _predictCsv,
              child: const Text("Subir CSV y predecir"),
            ),
            const SizedBox(height: 20),
            if (errorMessage.isNotEmpty)
              Text(errorMessage, style: const TextStyle(color: Colors.red)),
            if (predictions != null)
              Expanded(
                child: ListView.builder(
                  itemCount: predictions!.length,
                  itemBuilder: (context, index) {
                    final item = predictions![index];
                    return Card(
                      margin: const EdgeInsets.symmetric(vertical: 4),
                      child: ListTile(
                        leading: Text("#${item["index"]}"),
                        title: Text(
                          "Predicción: ${item["prediction"] == 1 ? "Churn" : "No Churn"}",
                          style: TextStyle(
                            color: item["prediction"] == 1
                                ? Colors.red
                                : Colors.green,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        subtitle: Text(
                          "Probabilidad: ${(item["probability"] * 100).toStringAsFixed(2)}%",
                        ),
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
