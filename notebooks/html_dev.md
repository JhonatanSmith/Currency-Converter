The first thing to be said is that, we need av ery simple html web page to compile all the info withing the page. 

This was build witha  very simple prompt from chat gpt like "look, i want a simple webpage to deploy a dataframe from a python api that i am developing. It requieres an input from the user ann bla bla"

And it gave us this web page to beging working with. Later, we will do some adjustment but from the moment, it's more than ok. 


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game Prices</title>
    <style>
        table.data {
            width: 100%;
            border-collapse: collapse;
        }
        table.data th, table.data td {
            border: 1px solid black;
            padding: 5px;
            text-align: center;
        }
    </style>
</head>

<!COMMENT: Until this point, this is just setting some default config to an HTML page. Title and a couple of details. 

The body will be like the core of what is going to have the page within it. -->

<body>
    <! This first section will create a header. And then we we wll give it form-->
    <h1>Insert game's name</h1>
    <! this tag will open a form to the user, to send info->
    <form method="post">
        <div id="game-inputs">
        <! The input: A text game inputed by user -->
            <input type="text" name="games">
        </div>
        <! Adding a new button-->
        <button type="button" onclick="addInput()">Add another game</button>
        <! The third button, to send the info-->
        <input type="submit" value="Search">
    </form>
    {% if tables %}
        <h2>Resultados del DataFrame</h2>
        {% for table in tables %}
            {{ table|safe }}
        {% endfor %}
    {% endif %}
    <script>
        function addInput() {
            var div = document.createElement('div');
            div.innerHTML = '<input type="text" name="games">';
            document.getElementById('game-inputs').appendChild(div);
        }
    </script>
</body>
</html>
