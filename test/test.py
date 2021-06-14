import os
import uv

def main():
    files = [os.path.join('test-data', i) for i in os.listdir('test-data')]
    data = [uv.BM3(i) for i in files]
    print(data[0].concs)


if __name__ == '__main__':
    main()
