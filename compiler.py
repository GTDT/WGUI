import json
import sys
import os


def check_json(JSON_DATA):

    for element in JSON_DATA['elements']:

        # Check if position values are integers
        if type(element['position']['x']) != int or type(element['position']['y']) != int:
            raise TypeError('Position values must be integers')

        # Check if size values are integers
        if type(element['size']['width']) != int or type(element['size']['height']) != int:
            raise TypeError('Size values must be integers')

        # Check if position values are positive
        if element['position']['x'] < 0 or element['position']['y'] < 0:
            raise ValueError('Position values must be positive')

        # Check if size values are greater than 0
        if element['size']['width'] <= 0 or element['size']['height'] <= 0:
            raise ValueError('Size values must be greater than 0')

    return True


def compileToCode(JSON_DATA):
    # --- Check if all required elements are present in the JSON file ---
    required_elements = ['window_title', 'window_size', 'elements']
    for element in required_elements:
        if element not in JSON_DATA:
            raise ValueError(
                f'Missing required element {element} in JSON file')

            # --- Generate C++ code ---
    cpp_code = f'''\
#include <QApplication>
#include <QLabel>
#include <QPushButton>
#include <QLineEdit>
#include <QVBoxLayout>

int main(int argc, char *argv[]) {{
    QApplication app(argc, argv);
    std::cout << "Opening GUI" << std::endl;

    // Create main window
    QWidget *mainWindow = new QWidget();
    mainWindow->setWindowTitle("{JSON_DATA['window_title']}");
    mainWindow->resize({JSON_DATA['window_size']['width']}, {JSON_DATA['window_size']['height']});

    // Create layout
    QVBoxLayout *layout = new QVBoxLayout();
'''

    for element in JSON_DATA['elements']:

        if element['type'] == 'label':
            cpp_code += f'''
    // label - id:{element['id']}
    QLabel *label{element['id']} = new QLabel("{element['text']}");
    label{element['id']}->move({element['position']['x']}, {element['position']['y']});
    layout->addWidget(label{element['id']});
'''

        if element['type'] == 'button':
            cpp_code += f'''
    // button id:{element['id']}
    QPushButton *button{element['id']} = new QPushButton("{element['text']}");
    button{element['id']}->move({element['position']['x']}, {element['position']['y']});
    layout->addWidget(button{element['id']});
'''

        if element['type'] == 'textbox':
            cpp_code += f'''
    // textbox id:{element['id']}
    QLineEdit *textbox{element['id']} = new QLineEdit();
    textbox{element['id']}->setPlaceholderText("{element['placeholder']}");
    textbox{element['id']}->move({element['position']['x']}, {element['position']['y']});
    textbox{element['id']}->resize({element['size']['width']}, {element['size']['height']});
    layout->addWidget(textbox{element['id']});
'''

    cpp_code += '''
    // Set layout
    mainWindow->setLayout(layout);
    mainWindow->show();
    std::cout << "GUI opened" << std::endl;
    return app.exec();
}
'''

    return cpp_code


def main(args):

    if len(args) < 3:
        print('Usage: python compiler.py <input_file> <output_file>')

    input_file = args[1]
    output_file = args[2]

    with open(input_file, 'r') as f:
        JSON_DATA = json.load(f)
        # for element in JSON_DATA['elements']:
        #     print(element['type'])

    # --- Check json ---
    print(f'Checking {input_file}...')
    # if not check_json(JSON_DATA):
    print('compiling...')
    compiled_code = compileToCode(JSON_DATA)

    # --- Write C++ code to file
    with open('launcher.cpp', 'w') as f:
        f.write(compiled_code)

    # --- Compile C++ code ---
    print('Compiling C++ code...')
    os.system(
        f'g++ {output_file} -o launcher -mwindows -std=c++20 -lQt5Core -lQt5Gui -lQt5Widgets -lQt5Network -lstdc++fs'
    )

    return 0


if __name__ == "__main__":
    main(sys.argv)
