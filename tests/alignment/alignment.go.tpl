package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

#CODE_TPL#

func sigmoid(x float64) float64 {
	return 1 / (1.0 + math.Exp(-x))
}

func main() {
	feature_path := "tests/data/feature.csv"
	answer_path := "tests/data/lgb_predict.csv"

	f, err := os.Open(feature_path)
	if err != nil {
		fmt.Printf("error, %v\n", err)
		os.Exit(1)
	}

	f2, err := os.Open(answer_path)
	if err != nil {
		fmt.Printf("error, %v\n", err)
		os.Exit(1)
	}
	buf := bufio.NewScanner(f)
	buf2 := bufio.NewScanner(f2)

	for {
		if !buf.Scan() || !buf2.Scan() {
			break
		}

		line := strings.TrimSpace(buf.Text())
		elements := strings.Split(line, ",")
		input := make([]float64, 11)
		answer, err := strconv.ParseFloat(strings.TrimSpace(buf2.Text()), 8)
		if err != nil {
			println("parse float error")
		}
		for i, element := range elements {
			if element == "nan" {
				input[i] = math.NaN()
			} else {
				value, err := strconv.ParseFloat(element, 8)
				if err != nil {
					fmt.Printf("error, %v\n", err)
					os.Exit(1)
				}
				input[i] = value
			}
		}
		res := sigmoid(predict_tree_all(input))
		fmt.Printf("%f, %f\n", res, answer)
		if math.Abs(res-answer) > 1e-6 {
			fmt.Printf("error, %v\n", err)
			os.Exit(1)
		}
	}
}
