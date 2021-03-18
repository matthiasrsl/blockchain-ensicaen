block_list = [];
ip_list = [];
new_blocks = [];
first_update = true;
message_list = [];

graph = null;

function loadJSON(path, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                return callback(JSON.parse(xhr.responseText));
            } else {
                console.log("Error");
            }
        }
    };
    xhr.open("GET", path, true);
    xhr.overrideMimeType("text/plain");
    xhr.send();
}

function formatHash(hash) {
    hash = String(hash);
    begin = hash.slice(0, -6);
    end = hash.slice(-6);
    return `${begin}<span class="hash_highlight">${end}</span>`
}

function shortHash(hash) {
    return hash.slice(-6);
}

function updateBlockchain(data) {
    blockchain = data.blockchain;

    container = document.querySelector("#block_list");

    for (block of blockchain) {
        if (!block_list.includes(block.hash)) {
            graph.commit({subject: `Height ${block.index}`, body: block.data, author: block.miner, hash: shortHash(block.hash)});


            block_list.push(block.hash);
        }
    }

    first_update = false;
}

/*function finishBlockTransition() {
    block_div = new_blocks.pop();
    while (block_div) {
        block_div.className = "block";
        block_div = new_blocks.pop();
    }
}*/

function updateNodes(data) {
    let node_section = document.getElementById("nodes");
    let nodes = data.nodes;

    for (node of nodes) {
        if (!ip_list.includes(node.ip)) {
            node_p = document.createElement("p");
            node_p.innerHTML = `
                <span class="node_name">${node.name}</span> <span class="node_ip">${node.ip}</span>
            `
            node_section.appendChild(node_p);
            ip_list.push(node.ip);
        }
    }
}

/*function updateMessages(data) {
    let message_section = document.getElementById("messages");
    let messages = data.messages;

    for(mess of messages) {
        message_p = document.createElement("p");
        message_p.innerHTML = `
            <span class="sender">${mess.sender}</span> <span class="content">${mess.content}</span> 
        `
        message_section.appendChild(message_p);
        message_list.push(mess.content);
    }
}*/

function initGitGraph() {
    container = document.querySelector("#block_list");
    graph = GitgraphJS.createGitgraph(container);
}

function main() {
    initGitGraph();
    var intervalId = setInterval(function () {
        console.log("Update !");
        //finishBlockTransition();
        loadJSON("http://localhost:8000/etc/visudata/blockchain.json", (data) => updateBlockchain(data));
        loadJSON("http://localhost:8000/etc/visudata/nodes.json", (data) => updateNodes(data));
        //loadJSON("messages.json", (data) => updateMessages(data));
    }, 5000);
}

main();