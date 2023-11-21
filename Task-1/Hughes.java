package com.aleksey;

import java.awt.*;
import java.io.*;
import java.math.BigInteger;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class Hughes {
    private static final class Alice {
        BigInteger x;
        BigInteger Y;
        BigInteger k;
    }

    private static final class Bob {
        BigInteger y;
        BigInteger X;
        BigInteger k;
        BigInteger z;
    }

    private static BigInteger generateStrongPrime() { // Генерация сильного простого числа p
        q = BigInteger.probablePrime(qSize, new Random()); // q вероятно-случайное (тест Миллера-Рабина), размером qSize бит
        BigInteger mod = BigInteger.probablePrime(2048, new Random()); // степень 2 вероятно-случайная
        BigInteger k = BigInteger.TWO;
        BigInteger res;
        while (true) {
            res = BigInteger.TWO.modPow(k, mod).multiply(q).add(BigInteger.ONE); //вычисление p=(2^k)*q+1
            if (res.isProbablePrime(20)) { //проверка на простое
                System.out.print("p = 2^" + k + " * " + q + " + 1 = ");
                return res; //вывод
            }
            k = k.add(BigInteger.ONE); // k + 1
        }
    }

    private static BigInteger q;
    private static int qSize = 32;
    public static BigInteger P;
    public static BigInteger G;

    private static void writeFile (String text, String filename) {
        try {
            File output = new File(filename);
            Files.deleteIfExists(Paths.get(filename));
            if (output.createNewFile()) {
                BufferedWriter out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(output), "UTF-8"));
                out.write(text);
                out.close();
            } else {
                System.out.println("Файл с таким именем уже существует или нет прав доступа к директории.");
                System.exit(-1);
            }
        } catch (IOException e ) {
            e.printStackTrace();
        }
    }

    private static List<BigInteger> readFile (String filename) {
        List<BigInteger> res = new ArrayList<>();

        try {
            File file = new File(filename);
            FileReader fr = new FileReader(file);
            BufferedReader reader = new BufferedReader(fr);
            String line = reader.readLine();
            while (line != null) {
                res.add(new BigInteger(line));
                line = reader.readLine();
            }
            fr.close();
        } catch (IOException e) {
            System.out.println("Не найден файл " + filename);
            System.exit(-1);
        }
        return res;
    }

    public static void main(String[] args) {
        String aliceFolder = args[0]; // Папки, где находятся файлы с g, p, q, X, Y, и т. д.
        String bobFolder = args[1];
        String sharedFolder = args[2];

        Scanner in = new Scanner(System.in);
        System.out.println("Введите роль: 0 - Алиса, 1 - Боб, 2 - генерирующий центр:");
        int role = in.nextInt();

        switch (role) {
            case 0 -> { // Часть Алисы
                Alice alice = new Alice();
                System.out.println("Введите режим работы: 0 - расчет, 1 - отправка");
                int mode = in.nextInt();
                P = readFile(sharedFolder.concat("\\p")).get(0);
                G = readFile(sharedFolder.concat("\\g")).get(0);
                if (mode == 0) { // 1 пункт алгоритма, Алиса генерирует сеансовый ключ (расчет)
                    String alice_k_file = "\\alice_k";
                    alice.x = new BigInteger(2048, new Random()).mod(P); // x из интервала от 1 до p
                    if (alice.x.compareTo(BigInteger.TWO) <= 0)
                        alice.x.add(BigInteger.ONE);
                    alice.k = G.modPow(alice.x, P); // alice_k = g^x mod p
                    System.out.println("Алиса сгенерировала x = " + alice.x + ", получила ключ k = " + alice.k);
                    writeFile(alice.k.toString(), aliceFolder.concat(alice_k_file));
                    writeFile(alice.x.toString(), aliceFolder.concat("\\alice_x"));
                } else { // 3 пункт алгоритма, A -> B
                    String xFile = "\\X";
                    BigInteger Y = readFile(bobFolder.concat("\\Y")).get(0);
                    BigInteger x = readFile(bobFolder.concat("\\alice_x")).get(0);
                    BigInteger X = Y.modPow(x, P);
                    writeFile(X.toString(), bobFolder.concat(xFile));
                    System.out.println("X = " + X);
                }

            }
            case 1 -> { // Часть Боба
                Bob bob = new Bob();
                System.out.println("Введите режим работы: 0 - расчет, 1 - отправка");
                int mode = in.nextInt();
                P = readFile(sharedFolder.concat("\\p")).get(0);
                G = readFile(sharedFolder.concat("\\g")).get(0);
                if (mode == 0) { // 4 пункт алгоритма, сеансовый ключ Боба K'
                    bob.y = readFile(bobFolder.concat("\\bob_y")).get(0);
                    bob.X = readFile(bobFolder.concat("\\X")).get(0);
                    bob.z = bob.y.modInverse(P.subtract(BigInteger.ONE));
                    bob.k = bob.X.modPow(bob.z, P);
                    writeFile(bob.k.toString(), aliceFolder.concat("\\bob_k"));
                    System.out.println("Боб вычисляет z = " + bob.z + " и ключ k' = " + bob.k);
                } else { // 2 пункт алгоритма, B -> A
                    bob.y = BigInteger.probablePrime(256, new Random()).mod(P);
                    BigInteger Y = G.modPow(bob.y, P);
                    System.out.println("Боб сгенерировал y = " + bob.y + ", послал Алисе Y = " + Y);
                    writeFile(Y.toString(), aliceFolder.concat("\\Y"));
                    writeFile(bob.y.toString(), bobFolder.concat("\\bob_y"));
                }
            }
            case 2 -> { // Часть генерирующего центра
                System.out.println("Введите длину q в битах (p = 2^k*q + 1):");
                qSize = in.nextInt();
                P = generateStrongPrime(); // Генерация сильного простого числа p
                System.out.println(P);
                Random r = new Random();
                G = BigInteger.probablePrime(P.bitLength() - 4, r);
                System.out.println("g = " + G);

                writeFile(P.toString(), sharedFolder.concat("\\p"));
                writeFile(G.toString(), sharedFolder.concat("\\g"));
                writeFile(q.toString(), sharedFolder.concat("\\q"));
            }
        }
    }
}

