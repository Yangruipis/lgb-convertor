#CODE_TPL#

#include <algorithm>
#include <cmath>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

using namespace std;

float sigmoid(float in) { return 1 / (1.0 + exp(-in)); }

int main()
{
    ifstream is_feat("tests/data/feature.csv");
    ifstream is_pred("tests/data/lgb_predict.csv");
    string str, token, pred;
    string delimiter = ",";
    size_t pos = 0;
    while (getline(is_feat, str))
    {
        getline(is_pred, pred);
        float arr[11];
        int count = 0;
        for (int count = 0; count < 11; count++)
        {
            pos = str.find(delimiter);
            token = str.substr(0, pos);
            str.erase(0, pos + delimiter.length());
            if (token == "nan")
            {
                arr[count] = std::nan("");
            }
            else
            {
                arr[count] = std::stof(token);
            }
            printf("%d %6.6lf\n", count, arr[count]);
        }
        auto res = sigmoid(predict_tree_all(arr));
        auto answer = std::stof(pred);
        printf("%6.4lf vs %6.4lf\n", res, answer);
        if (std::abs(res - answer) > 1e-6)
            throw std::runtime_error("not equal ");
    }
    return 0;
}
