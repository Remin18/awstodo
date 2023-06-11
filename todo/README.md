# Todo

## AWSへのデプロイ
```bash
sam deploy --stack-name "todo" --capabilities CAPABILITY_NAMED_IAM
```

## API

### Auth
ユーザー作成
```yaml
      Events:
        CreateUser:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /create
            Method: post
```

ユーザーパスワード変更
```yaml
      Events:
        ConfirmUser:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /confirm
            Method: post
```

IDトークン取得
```yaml
      Events:
        AuthUser:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /auth
            Method: post
```

### User
ユーザー作成
```yaml
      Events:
        CreateUserData:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /user
            Method: post
            Auth:
              Authorizer: CognitoAuthorizer
```

ユーザープロフィール
```yaml
      Events:
        CreateUserData:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /user
            Method: get
            Auth:
              Authorizer: CognitoAuthorizer
```

### Todo
Todo一覧
```yaml
      Events:
        ListTodo:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /todo
            Method: get
            Auth:
              Authorizer: CognitoAuthorizer
```

Todo作成
```yaml
      Events:
        CreateTodo:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /todo
            Method: post
            Auth:
              Authorizer: CognitoAuthorizer
```

Todo更新
```yaml
      Events:
        UpdateTodo:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /todo/{todo_id}
            Method: put
            Auth:
              Authorizer: CognitoAuthorizer
```

Todo削除
```yaml
      Events:
        DeleteTodo:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /todo/{todo_id}
            Method: delete
            Auth:
              Authorizer: CognitoAuthorizer
```

Todo検索
```yaml
      Events:
        SearchTodo:
          Type: Api
          Properties:
            RestApiId: !Ref ApiGateway
            Path: /todo/search/{word}
            Method: get
            Auth:
              Authorizer: CognitoAuthorizer
```

## 削除
```bash
sam delete --stack-name "todo"
```
