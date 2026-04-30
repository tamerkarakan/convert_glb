async function getComfyApp() {
    const comfyApi = globalThis.comfyAPI;
    const app = comfyApi?.app?.app ?? comfyApi?.app;
    if (app?.registerExtension) {
        return app;
    }

    const legacy = await import("../../scripts/app.js");
    return legacy.app;
}

function selectGlbFile() {
    return new Promise((resolve) => {
        const input = document.createElement("input");
        input.type = "file";
        input.accept = ".glb,.gltf,model/gltf-binary,model/gltf+json";
        input.style.display = "none";
        input.onchange = () => {
            resolve(input.files?.[0] ?? null);
            input.remove();
        };
        document.body.appendChild(input);
        input.click();
    });
}

async function uploadGlbFile(file) {
    const body = new FormData();
    body.append("file", file);

    const fetchApi =
        globalThis.comfyAPI?.api?.api?.fetchApi ??
        globalThis.comfyAPI?.api?.fetchApi ??
        globalThis.fetch.bind(globalThis);

    const response = await fetchApi("/convert_glb/upload", {
        method: "POST",
        body,
    });

    const result = await response.json();
    if (!response.ok) {
        throw new Error(result?.error ?? "GLB upload failed.");
    }
    return result.path;
}

function createPickerWidget(node, pathWidget) {
    const container = document.createElement("div");
    const button = document.createElement("button");

    container.style.width = "100%";
    container.style.boxSizing = "border-box";

    button.type = "button";
    button.textContent = "Choose GLB/GLTF";
    button.style.width = "100%";
    button.style.boxSizing = "border-box";
    button.style.border = "1px solid #555";
    button.style.borderRadius = "4px";
    button.style.padding = "6px 8px";
    button.style.background = "#2b2b2b";
    button.style.color = "#ddd";
    button.style.cursor = "pointer";

    button.addEventListener("click", async (event) => {
        event.preventDefault();
        event.stopPropagation();

        const file = await selectGlbFile();
        if (!file) {
            return;
        }

        try {
            button.disabled = true;
            button.textContent = "Uploading...";
            pathWidget.value = await uploadGlbFile(file);
            pathWidget.callback?.(pathWidget.value);
            node.graph?.setDirtyCanvas(true, true);
        } catch (error) {
            console.error("[convert_glb]", error);
            alert(error.message ?? "GLB upload failed.");
        } finally {
            button.disabled = false;
            button.textContent = "Choose GLB/GLTF";
        }
    });

    container.appendChild(button);

    const widget = node.addDOMWidget("choose_glb", "GLB_FILE_PICKER", container, {
        getValue() {
            return "";
        },
        setValue() {},
        getMinHeight() {
            return 32;
        },
    });
    widget.serialize = false;
}

const app = await getComfyApp();

app.registerExtension({
    name: "convert_glb.file_picker",
    nodeCreated(node) {
        if (node.comfyClass !== "GLBFilePicker") {
            return;
        }

        const pathWidget = node.widgets?.find((widget) => widget.name === "glb_path");
        if (pathWidget) {
            createPickerWidget(node, pathWidget);
        }
    },
});
