        c.Div(
            components=[
                c.Heading(text='Code', level=2),
                c.Code(
                    language='python',
                    text="""

#create thread
thread = client.beta.threads.create()
#add a message to the thread
message = client.beta.threads.messages.create(
thread_id=thread.id,
role="user",
content="we can talk about what should go here"
#run the thread
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)
#wait for the thread to finish running
import time

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

run = wait_on_run(run, thread)

#return the results

messages = client.beta.threads.messages.list(thread_id=thread.id)

#run an assistant
from openai import OpenAI

ASSISTANT_ID = assistant.id  # or a hard-coded ID like "asst-..."

client = OpenAI()

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

client.beta.threads.create_and_run()
""",
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Link List', level=2),
                c.Markdown(
                    text=(
                        'This is a simple unstyled list of links, '
                        '\n\n'
                        'LinkList is also used in `Navbar` and `Pagination`.'
                    )
                ),
                c.LinkList(
                    links=[
                        c.Link(
                            components=[c.Text(text='Internal Link - the the home page')],
                            on_click=GoToEvent(url='/'),
                        ),
                        c.Link(
                            components=[c.Text(text='Pydantic (External link)')],
                            on_click=GoToEvent(url='https://pydantic.dev'),
                        ),
                        c.Link(
                            components=[c.Text(text='Assistants API Overview')],
                            on_click=GoToEvent(url='https://cookbook.openai.com/examples/assistants_api_overview_python')
                        )
                    ],
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Button and Modal', level=2),
                c.Paragraph(text='The button below will open a modal with static content.'),
                c.Button(text='Show Static Modal', on_click=PageEvent(name='static-modal')),
                c.Modal(
                    title='Static Modal',
                    body=[c.Paragraph(text='This is some static content that was set when the modal was defined.')],
                    footer=[
                        c.Button(text='Close', on_click=PageEvent(name='static-modal', clear=True)),
                    ],
                    open_trigger=PageEvent(name='static-modal'),
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Dynamic Modal', level=2),
                c.Markdown(
                    text=(
                        'The button below will open a modal with content loaded from the server when '
                        "it's opened using `ServerLoad`."
                    )
                ),
                c.Button(text='Show Dynamic Modal', on_click=PageEvent(name='dynamic-modal')),
                c.Modal(
                    title='Dynamic Modal',
                    body=[c.ServerLoad(path='/components/dynamic-content')],
                    footer=[
                        c.Button(text='Close', on_click=PageEvent(name='dynamic-modal', clear=True)),
                    ],
                    open_trigger=PageEvent(name='dynamic-modal'),
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Server Load', level=2),
                c.Paragraph(text='Even simpler example of server load, replacing existing content.'),
                c.Button(text='Load Content from Server', on_click=PageEvent(name='server-load')),
                c.Div(
                    components=[
                        c.ServerLoad(
                            path='/components/dynamic-content',
                            load_trigger=PageEvent(name='server-load'),
                            components=[c.Text(text='before')],
                        ),
                    ],
                    class_name='py-2',
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Server Load SSE', level=2),
                c.Markdown(
                    text=(
                        '`ServerLoad` can also be used to load content from an SSE stream.\n\n'
                        "Here the response is the streamed output from OpenAI's GPT-4 chat model."
                    )
                ),
                c.Button(text='Load SSE content', on_click=PageEvent(name='server-load-sse')),
                c.Div(
                    components=[
                        c.ServerLoad(
                            path='/components/sse',
                            sse=True,
                            load_trigger=PageEvent(name='server-load-sse'),
                            components=[c.Text(text='before')],
                        ),
                    ],
                    class_name='my-2 p-2 border rounded',
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Iframe', level=2),
                c.Markdown(text='`Iframe` can be used to embed external content.'),
                c.Iframe(src='https://pydantic.dev', width='100%', height=400),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Image', level=2),
                c.Paragraph(text='An image component.'),
                c.Image(
                    src='https://avatars.githubusercontent.com/u/110818415',
                    alt='Pydantic Logo',
                    width=200,
                    height=200,
                    loading='lazy',
                    referrer_policy='no-referrer',
                    class_name='border rounded',
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Video', level=2),
                c.Paragraph(text='A video component.'),
                c.Video(
                    sources=['https://www.w3schools.com/html/mov_bbb.mp4'],
                    autoplay=False,
                    controls=True,
                    loop=False,
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Custom', level=2),
                c.Markdown(
                    text="""\
Below is a custom component, in this case it implements [cowsay](https://en.wikipedia.org/wiki/Cowsay),
but you might be able to do something even more useful with it.

The statement spoken by the famous cow is provided by the backend."""
                ),
                c.Custom(data='This is a custom component', sub_type='cowsay'),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        title='Components',
    )


@router.get('/dynamic-content', response_model=FastUI, response_model_exclude_none=True)
async def modal_view() -> list[AnyComponent]:
    await asyncio.sleep(0.5)
    return [c.Paragraph(text='This is some dynamic content. Open devtools to see me being fetched from the server.')]

# class MessageForm(BaseModel):
#     message= Field(title='message', description='Enter whatever value you like')

# async def append_message_form(thread_id: str) -> list[AnyComponent]:
#     await asyncio.sleep(0.5)

#     message_form = c.ModelForm(model=MessageForm, submit_url='/api/append-message', submit_trigger=PageEvent(name='submit-message'))

#     return demo_page(
#         c.Div(
#             components=[
#                 c.Heading(text='Append Message to Thread', level=2),
#                 c.Text(text=f'Thread ID: {thread_id}'),
#                 message_form,
#             ]
#         ),
#     )
