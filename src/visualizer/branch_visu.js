block_list = [];
block_div_list = new Map();
block_map = new Map();
branch_map = new Map();
branch_block_map = new Map();
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

    container = document.querySelector("#branch_list");
    bk_section = document.querySelector("#block_list");
    /*container.firstElementChild.remove();

    graph = initGitGraph();*/

    for (block of blockchain) {
        if (!block_list.includes(block.hash)) {
            block_div = document.createElement("div");
            if (first_update) {
                block_div.className = `block branch_${block.branch}`
            } else {
                block_div.className = `block appearing branch_${block.branch}`
            }
            block_div.id = `block_${block.hash}`

            block_div.innerHTML = `
                <h2>Block #${shortHash(block.hash)}</h2>
                <p class="block_info">
                    <strong class="hash_label">Hash</strong> <span class="hash">${formatHash(block.hash)}</span> 
                </p>

                <p class="block_info">
                    <strong>Height</strong> ${block.index}
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
                    <strong>Mined by</strong> ${block.miner}
                </p>

                <p class="block_info">
                    <strong>Branch</strong> ${block.branch}
                </p>

                <p class="block_info">
                    <strong>Data</strong>
                </p>

                <div class="data_container">
                    <pre class="block_data">${JSON.stringify(block.data, null, 4)}</pre>
                </div>
                </p>
            `


            if (block.previous_hash) {
                try {
                    var branch = branch_map[`branch${block.branch}`];
                    branch.commit({
                        subject: `Height ${block.index}`, 
                        body: block.data, 
                        author: block.miner, 
                        hash: shortHash(block.hash),
                        onMessageClick: (e) => displayBlock(e),
                    });
                    var new_block_branch = graph.branch(shortHash(block.hash));
                    branch_block_map[block.hash] = new_block_branch;
                    console.log(`Block ${shortHash(block.hash)} added to branch id: ${block.branch} (already present)`);
                } catch {
                    var parent_branch = branch_block_map[block.previous_hash];
                    var new_branch = graph.branch({name: `branch${block.branch}`, parentBranch: parent_branch});
                    parent_branch.commit({
                        subject: `Height ${block.index}`, 
                        body: `${block.data}\n${block.previous_hash}`, 
                        author: block.miner, 
                        hash: shortHash(block.hash),
                        onMessageClick: (e) => displayBlock(e),
                    });
                    var new_block_branch = graph.branch(shortHash(block.hash));
                    branch_block_map[block.hash] = new_block_branch;
                    branch_map[`branch${block.branch}`] = parent_branch;
                    console.log(`Block ${shortHash(block.hash)} to branch id: ${block.branch} (created) (parent branch: ${block.previous_hash})`);
                }

                
            } else {
                var origin_branch = graph.branch(shortHash(block.hash));
                branch_map[`branch${block.branch}`] = origin_branch;
                branch_block_map[block.hash] = origin_branch;
                console.log(`Origin branch id: ${block.branch}`);
                origin_branch.commit({
                    subject: `Height ${block.index}`, 
                    body: block.data, 
                    author: block.miner, 
                    hash: shortHash(block.hash),
                    onMessageClick: (e) => displayBlock(e),
                });
            }

            block_div_list[shortHash(block.hash)] = block_div;


            bk_section.appendChild(block_div);
            block_list.push(block.hash);
            new_blocks.push(block_div)
            block_map[block.hash] = block;
        }
    }

    first_update = false;
}

function displayBlock(e) {
    console.log(e);
    e.commit({
        subject: `Test branch`, 
        body: "body", 
        author: "block.miner", 
    });
    selected_block_div = document.querySelector("#selected_block");
    try {
        selected_block_div.firstElementChild.remove();
    } catch (error) {
        ;
    }
    selected_block_div.appendChild(block_div_list[e.hash]);
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
    container = document.querySelector("#branch_list");
    graph = GitgraphJS.createGitgraph(container);

    return graph;
}

function displayBranches(e) {
    var block_section = document.querySelector("#block_list");
    var branch_section = document.querySelector("#branch_list");
    var block_button = document.querySelector("#normal_visu_button");
    var branch_button = document.querySelector("#branch_visu_button");

    block_section.style.display = "none";
    branch_section.style.display = "block";
    block_button.className = "mainbutton";
    branch_button.className = "mainbutton selected";
}

function displayBlocks(e) {
    var block_section = document.querySelector("#block_list");
    var branch_section = document.querySelector("#branch_list");
    var block_button = document.querySelector("#normal_visu_button");
    var branch_button = document.querySelector("#branch_visu_button");

    block_section.style.display = "flex";
    branch_section.style.display = "none";
    block_button.className = "mainbutton selected";
    branch_button.className = "mainbutton";
}

function main() {
    initGitGraph();

    var block_button = document.querySelector("#normal_visu_button");
    var branch_button = document.querySelector("#branch_visu_button");
    block_button.addEventListener("click", (e) => displayBlocks(e));
    branch_button.addEventListener("click", (e) => displayBranches(e));

    var intervalId = setInterval(function () {
        loadJSON("http://localhost:8000/etc/visudata/blockchain.json", (data) => updateBlockchain(data));
        loadJSON("http://localhost:8000/etc/visudata/nodes.json", (data) => updateNodes(data));
        //loadJSON("messages.json", (data) => updateMessages(data));
    }, 2000);
}

main();