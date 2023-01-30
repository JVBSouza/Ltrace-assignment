#include <iostream>
#include <map>
#include <fstream>
#include <vector>
#include <algorithm>

int main(int argc, char **argv) {
    for(int i = 1; i < argc; ++i) {

        std::ifstream file(argv[i]);
        std::cout << argv[i] << std::endl;

        std::map<const char, int> map;

        char letter;
        while(file >> letter) {
            if (letter >= 'A' && letter <= 'Z') letter += 32;
            if (letter < 'a' || letter > 'z') continue;

            if (map.find(letter) == map.end()){
                map.insert(std::pair<char, int>(letter, 1));
            } else {
                map[letter]++;
            }
        }

        std::vector<std::pair<char, int>> pairs;
        for (auto itr = map.begin(); itr != map.end(); ++itr)
            pairs.push_back(*itr);

        sort(pairs.begin(), pairs.end(), [](std::pair<char, int>& a, std::pair<char, int>& b){
            return a.second > b.second;
        });

        for (const auto& pair : pairs) {
            std::cout << pair.first << " " << pair.second << std::endl;
        }

        std::cout << "" << std::endl;
        file.close();
    }
}
