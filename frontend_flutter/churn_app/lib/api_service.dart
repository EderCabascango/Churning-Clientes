import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:file_picker/file_picker.dart';

class ApiService {
  final String baseUrl = "http://192.168.1.51:8000";

  /// Predicción para un solo cliente (JSON)
  Future<Map<String, dynamic>> getPrediction(
    Map<String, dynamic> inputData,
  ) async {
    final url = Uri.parse('$baseUrl/predict/');
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode(inputData),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Error en la API: ${response.statusCode}");
    }
  }

  /// 🚀 Subir CSV y obtener predicciones (Web-friendly)
  Future<List<Map<String, dynamic>>> uploadCsvAndPredict() async {
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['csv'],
      withData: true, // ⚡ necesario para Web
    );

    if (result != null) {
      final bytes = result.files.single.bytes;
      final fileName = result.files.single.name;

      if (bytes == null) {
        throw Exception("No se pudieron leer los bytes del archivo.");
      }

      var request = http.MultipartRequest(
        "POST",
        Uri.parse("$baseUrl/predict_csv/"),
      );

      request.files.add(
        http.MultipartFile.fromBytes("file", bytes, filename: fileName),
      );

      var response = await request.send();

      if (response.statusCode == 200) {
        final respStr = await response.stream.bytesToString();
        final data = jsonDecode(respStr);
        return List<Map<String, dynamic>>.from(data["results"]);
      } else {
        throw Exception("Error en la API: ${response.statusCode}");
      }
    } else {
      throw Exception("No se seleccionó ningún archivo.");
    }
  }
}
