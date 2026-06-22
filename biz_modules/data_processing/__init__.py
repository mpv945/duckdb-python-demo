

def main():
    print("====== 程序启动 ======")

    # 调用不同目录下的业务
    is_login = process_user_login("张三")
    if is_login:
        result = process_payment(199.99)
        print(f"支付状态: {result}")


if __name__ == '__main__':
    main()