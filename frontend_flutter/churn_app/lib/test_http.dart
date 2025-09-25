import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const HttpTestApp());
}

class HttpTestApp extends StatelessWidget {
  const HttpTestApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "HTTP Test",
      theme: ThemeData(primarySwatch: Colors.blue),
      home: HttpTestScreen(),
    );
  }
}

class HttpTestScreen extends StatefulWidget {
  @override
  _HttpTestScreenState createState() => _HttpTestScreenState();
}

class _HttpTestScreenState extends State<HttpTestScreen> {
  String result = "Presiona el botón para hacer GET";

  Future<void> fetchData() async {
    final url = Uri.parse("https://jsonplaceholder.typicode.com/posts/1");
    final response = await http.get(url);

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      setState(() {
        result = data.toString();
      });
    } else {
      setState(() {
        result = "Error: ${response.statusCode}";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Prueba HTTP")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: fetchData,
              child: const Text("Hacer GET"),
            ),
            const SizedBox(height: 20),
            Text(result),
          ],
        ),
      ),
    );
  }
}
