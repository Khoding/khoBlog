EDITORJS_DEFAULT_PLUGINS = (
    '@editorjs/paragraph',
    '@editorjs/header',
    '@editorjs/list',
    '@editorjs/checklist',
    '@editorjs/quote',
    '@editorjs/raw',
    '@editorjs/code',
    '@editorjs/inline-code',
    '@editorjs/embed',
    '@editorjs/delimiter',
    '@editorjs/warning',
    '@editorjs/link',
    '@editorjs/marker',
    '@editorjs/table',
)

EDITORJS_DEFAULT_CONFIG_TOOLS = {
    'LinkTool': {
        'class': 'LinkTool',
        'inlineToolbar': True,
        'config': {"endpoint": '/editorjs/link_fetching/'},
        'shortcut': 'CMD+SHIFT+L'
    },
    'Header': {
        'class': 'Header',
        'inlineToolbar': True,
        'config': {
            'placeholder': 'Enter a header',
            'levels': [2, 3, 4],
            'defaultLevel': 2,
        }
    },
    'Checklist': {'class': 'Checklist', 'inlineToolbar': True},
    'List': {'class': 'List', 'inlineToolbar': True},
    'Quote': {'class': 'Quote', 'inlineToolbar': True},
    'Raw': {'class': 'RawTool'},
    'Code': {'class': 'CodeTool'},
    'InlineCode': {'class': 'InlineCode'},
    'Embed': {'class': 'Embed'},
    'Delimiter': {'class': 'Delimiter'},
    'Warning': {'class': 'Warning', 'inlineToolbar': True},
    'Marker': {'class': 'Marker', 'inlineToolbar': True},
    'Table': {'class': 'Table', 'inlineToolbar': True},
}