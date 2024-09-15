function display_filtered_tools(tools) { 
    if (tools) {
        $(".tool_filter .filtered").text(tools.join(", "));
    }
    else {
        $(".tool_filter .filtered").html("&nbsp;");
    }
 }

function display_filtered_categories(categories) { 
    if (categories) {
        $(".category_filter .filtered").text(categories.join(", "));
    }
    else {
        $(".category_filter .filtered").html("&nbsp;");
    }
 }



 function filter_projects (categories, tools) {
    $.ajax({
        url: "http://127.0.0.1:5001/api/v1/project_search",
        type: "POST",
        data: JSON.stringify({
            categories: categories,
            tools: tools
        }),
        contentType: "application/json",
        success: (projects) => {
            $("section.explore").html("");

                    $.each(projects, (idx, project) => {
                        $.ajax({
                            url: `http://127.0.0.1:5001/api/v1/users/${project.user_id}`,
                            type: "GET",
                            success: (user) => {
            
                                $("section.explore").append(`
                                <article class="${project.name}">
                                <img class="poster" src="../static/images/${project.name}_poster.jpg?{{ cache_id }}"
                                loading="lazy" decoding="async">
                                </img>
                                <div class="data">
                                    <a href="/projects/${project.name}" target="_blank">
                                        <p class="project-name">${project.name}</p>
                                    </a>
                                    <p class="category">Category: ${project.category}</p>
                                    <p class="developer"><span>Developer:</span> <a href="/users/${user.username}/projects" targer="_blank">${user.username}</a></p>
                                    <p class="tools">tools:</p>
                                    <p class="rate">Rate: ${project.rate} / 5.0</p>
                                    <p class="description">Description:</p>
                                    <div class="description_text">
                                        ${project.description}
                                    </div>
                                </div>
                            </article>
                            `);
                        
                            $.each(project.tools, (idx, tool) => {
                                if (tool == project.tools[-1]) {
                                    $("section.explore .data .tools").append(`${tool.name},&nbsp;`);
                                }
                                else {
                                    $("section.explore .data .tools").append(`${tool.name}`)
                                }
                                }
                            );
                    }
                    });
                }
            );
        }
    });
};


$(function () {
    const tools_dict = {};
    $(".tool_filter .drop_down input").on("click", function () {
        const isChecked = $(this).is(":checked");
        const tool_id = $(this).attr("data-id");
        const tool_name = $(this).attr("data-name");
        if (isChecked) {
            tools_dict[tool_id] = tool_name;   
        }
        else {
            delete tools_dict[tool_id];
        }
        display_filtered_tools(Object.values(tools_dict));
    })

    const categories_dict = {};
    $(".category_filter .drop_down input").on("click", function () {
        const isChecked = $(this).is(":checked");
        const category_id = $(this).attr("data-id");
        const category_name = $(this).attr("data-name");
        if (isChecked) {
            categories_dict[category_id] = category_name;
        }
        else {
            delete categories_dict[category_id];
        }
        display_filtered_categories(Object.values(categories_dict));
    });

    let tool_ids = []
    let category_ids = [];
    $(".search-bar .search-icon").on("click", () => {
        category_ids = Object.keys(categories_dict);
        tool_ids = Object.keys(tools_dict);
        
        $("section.categories article.focus").removeClass("focus");
        filter_projects(category_ids, tool_ids);
    });

    let categories = [];
    let index;
    $("section.categories article").on("click", function () {
        const isFocusOn = $(this).hasClass("focus");
        if (isFocusOn) {
            $(this).removeClass("focus");
            index = categories.indexOf($(this).attr("data-id"));
            categories.splice(index, 1);
        }
        else {
            // $("section.categories article.focus").removeClass("focus");
            $(this).addClass("focus");
            categories.push($(this).attr("data-id"));
        }
        // $("section.explore").html("");
        console.log(categories);
        filter_projects(categories, []);
    })
})


// $(function () {})

// -----------------------------
