# API Documentation

# 📁 Main Routes

## End-point: Hello World

### Method: GET

> ```
> /
> ```

### Response
```
{
    "message": "Hello world!"
}
```


## End-point: Feed

### Method: GET

> ```
> /feed
> ```

### Headers

| Content-Type | Value            |
| ------------ | ---------------- |
| Content-Type | application/json |

### Query Params

| Param | value       | Description   |
| ----- | ----------- | ------------- |
| page  | 50           | Page number   |
| limit | 1           | Count in page |
| vote  | ASC \| DESC | Sort by       |
| date  | ASC \| DESC | Sort by       |

# 📁 Authentication

## End-point: Get User Details From JWT

### Method: GET

> ```
> /user
> ```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |

## End-point: LogOut User

### Method: DELETE

> ```
> /auth/logout
> ```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


## End-point: Refresh User

### Method: POST

> ```
> /auth/refresh
> ```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


## End-point: Register Event

### Method: POST

> ```
> /auth/register
> ```

### Body (**raw**)

```json
{
  "name": "A. Ahmet Durmaz",
  "email": "ahmet@example.com",
  "password": "12345678"
}
```

### 🔑 Authentication noauth


## End-point: Update User

### Method: PUT

> ```
> /user/{ObjectID}
> ```

### Body (**raw**)

```json
{
  "name": "Updated Name",
  "email": "updated@email.com",
  "password": "updated_pass"
}
```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


## End-point: Delete User

### Method: DELETE

> ```
> /user
> ```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


## End-point: Login Event

### Method: POST

> ```
> /auth/login
> ```

### Body (**raw**)

```json
{
  "email": "ahmet@example.com",
  "password": "12345678"
}
```

### 🔑 Authentication noauth


# 📁 Posts

## End-point: Create Post

### Method: POST

> ```
> /post
> ```

### Body (**raw**)

```json
{
  "title": "Consequat non voluptate veniam ipsum sint ad do enim.",
  "content": "Pariatur id do ex ullamco culpa incididunt fugiat deserunt duis amet id irure magna nisi. Consequat dolore sint adipisicing ut nisi dolore non duis et esse enim id reprehenderit excepteur. Sint ullamco fugiat do qui ut magna deserunt anim irure esse. Nisi dolor adipisicing deserunt tempor ex veniam. Nulla consectetur sunt commodo voluptate cillum ut amet cillum nostrud ipsum."
}
```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


## End-point: Delete Post

### Method: DELETE

> ```
> /post/{PostID}
> ```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


## End-point: Update Post

### Method: PUT

> ```
> /post/{PostID}
> ```

### Body (**raw**)

```json
{
  "title": "Voluptate officia sit qui Lorem aliqua fugiat ipsum occaecat laboris ad id.",
  "content": "Minim ipsum dolore Lorem fugiat nisi aute ullamco enim. Ea dolor aliqua cillum nostrud officia magna laborum cillum eu duis. Incididunt amet nisi est cupidatat culpa proident. Sunt eiusmod do ex nostrud ex amet commodo labore sit magna. Incididunt deserunt id proident ut id exercitation ipsum ad exercitation."
}
```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


## End-point: Get Post Details via ID

### Method: GET

> ```
> /post/{PostID}
> ```

### 🔑 Authentication noauth


## End-point: Get Post Details via URL

### Method: GET

> ```
> /post/{PostURL}
> ```

```
Example: /post/vero-accusantium-doloremque-et-quas-quis-eos-minus-et-202401177387
```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


## End-point: Get User Posts

### Method: GET

> ```
> /post
> ```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


# 📁 Vote

## End-point: Create & Update & Delete Vote

### Method: POST

> ```
> /vote
> ```

### Body (**raw**)

```json
{
  "post_id": "{PostID}",
  "vote_value": -1
}
// You can update vote values with same POST request.
```
### Body parameters

| Param | Allowed Values | Type   |
| ----- | ----- | ------ |
| post_id | {PostID}   | ObjectID |
| vote_value | -1, 0, 1   | Integer |

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


# 📁 Comments

## End-point: Get Comments

### Method: GET

> ```
> /comment/{PostID}
> ```
> List comments of the post.

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


## End-point: Create Comment

### Method: POST

> ```
> /comment
> ```

### Body (**raw**)

```json
{
  "post_id": "{PostID}",
  "content": "Commodo reprehenderit eiusmod consequat dolor ad. Deserunt exercitation in commodo exercitation minim in officia consequat aute adipisicing velit est. Consectetur pariatur laboris nostrud non ex magna proident aliquip incididunt aute magna consectetur. Fugiat amet irure quis incididunt occaecat aute magna exercitation aliqua excepteur elit ad eu. Do sit proident cupidatat id dolore laboris velit non sint."
}
```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


## End-point: Update Comment

### Method: PUT

> ```
> /comment/{CommentID}
> ```

### Body (**raw**)

```json
{
  "content": "Est elit Lorem laborum ut anim magna laboris aute culpa mollit. Adipisicing enim ut exercitation laboris pariatur do officia eu sunt laboris voluptate. Nisi nostrud magna velit anim."
}
```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |


## End-point: Delete Comment

### Method: DELETE

> ```
> /comment/{CommentID}
> ```

### 🔑 Authentication bearer

| Param | value | Type   |
| ----- | ----- | ------ |
| token | JWT   | string |
