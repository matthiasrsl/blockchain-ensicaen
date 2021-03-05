block_list = [];
ip_list = [];
new_blocks = [];
first_update = true;

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

function updateBlockchain(data) {
    blockchain = data.blockchain;

    bk_section = document.querySelector("#block_list");

    for (block of blockchain) {
        if (!block_list.includes(block.hash)) {
            block_div = document.createElement("div");
            if (first_update) {
                block_div.className = "block"
            } else {
                block_div.className = "block appearing"
            }
            block_div.id = `block_${block.hash}`

            block_div.innerHTML = `
                <h2>Block #${block.index}</h2>
                <p class="block_info">
                    <strong class="hash_label">Hash</strong> <span class="hash">${formatHash(block.hash)}</span> 
                </p>

                <p class="block_info">
                    <strong>Previous hash</strong> 
                    <span class="hash_previous">${formatHash(block.previous_hash)}</span>
                </p>

                <p class="block_info">
                    <strong>Nonce</strong> ${block.nonce} 
                </p>

                <p class="block_info">
                    <strong>Timestamp</strong> ${block.date} 
                </p>

                <p class="block_info">
                    <strong>Data</strong>
                </p>

                <div class="data_container">
                    <pre class="block_data">${JSON.stringify(block.data, null, 4)}</pre>
                </div>
                </p>
            `

            bk_section.appendChild(block_div);
            //block_div.className = "block";
            block_list.push(block.hash);
            new_blocks.push(block_div);
            //setTimeout((e) => { block_div.className = "block" }, 1000, block_div)
        }
    }

    first_update = false;
}

function finishBlockTransition() {
    block_div = new_blocks.pop();
    while (block_div) {
        block_div.className = "block";
        block_div = new_blocks.pop();
    }
}

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

function main() {
    var intervalId = setInterval(function () {
        console.log("Update !");
        finishBlockTransition();
        loadJSON("http://localhost:8000/etc/visudata/blockchain.json", (data) => updateBlockchain(data));
        loadJSON("http://localhost:8000/etc/visudata/nodes.json", (data) => updateNodes(data));
        //loadJSON("messages.json", (data) => updateMessages(data));
    }, 200);
}

main();