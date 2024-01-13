from __future__ import annotations as _annotations

import asyncio

from fastapi import APIRouter
from fastui import AnyComponent, FastUI
from fastui import components as c
from fastui.events import GoToEvent, PageEvent
from openai import OpenAI
from .shared import demo_page
from pydantic import BaseModel, Field
from . import db

router = APIRouter()


def panel(*components: AnyComponent) -> AnyComponent:
    return c.Div(class_name='col border rounded m-1 p-2 pb-3', components=list(components))

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get('', response_model=FastUI, response_model_exclude_none=True)
async def components_view() -> list[AnyComponent]:
    return demo_page(
        c.Div(
            components=[
                c.Heading(text='Server Load', level=2),
                c.Paragraph(text='Even simpler example of server load, replacing existing content.'),
                c.Form(
                    display_mode=None,
                    submit_url='/',
                    form_fields=[c.FormFieldInput(name='test', title=f'Thread ID: is abstracted away for now', initial='data')],
                ),
                c.Button(text='Shows that we created and managed to store a thread id in our db', on_click=PageEvent(name='server-load-thread-info')),
                c.Div(
                    components=[
                        c.ServerLoad(
                            path='/components/thread-content',
                            load_trigger=PageEvent(name='server-load-thread-info'),
                            components=[
                                c.Text(text='''I've not got a single clue of where I'm going with this project.  We created logic that creates and stores thread ids in our server.  We've got a few of them made.  Currently we are just accessing the most recently created one. The next step is to do something with the thread.  I want to become proficient and articulate with managing threads and messages.  ''')],
                        ),
                    ],
                    class_name='py-2',
                ),
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Text', level=2),
                c.Text(text='OpenAI Assistants API and FastUI'),
            ]
        ),
        c.Form(
                submit_url='/',
                form_fields=[c.FormFieldInput(name='test', title=f'Thread ID: is abstracted away for now', initial='data')],
                footer=[
                    c.Button(text='Submit', on_click=PageEvent(name='append-message-to-thread')),
                ]
            ),
        c.Div(
            components=[
                c.Heading(text='OpenAI Assistants API and FastUI', level=2),
                c.Paragraph(text='Step one.'),
                c.Text(text='''learn what's going on well enough to make small changes that don'\t break the site''')
            ],
            class_name='border-top mt-3 pt-1',
        ),
        c.Div(
            components=[
                c.Heading(text='Why FastUI?', level=2),
                c.Heading(text='This is an H3', level=3),
                c.Heading(text='This is an H4', level=4),
                c.Text(text='''because i trust pydantic to do things in such a way as to be as succinct and easy to understand as possible while still operating within python''')
            ],
            class_name='border-top mt-3 pt-1',
        ),
    )

@router.get('/dynamic-content', response_model=FastUI, response_model_exclude_none=True)
async def modal_view() -> list[AnyComponent]:
    await asyncio.sleep(0.5)
    return [c.Paragraph(text='This is some dynamic content. Open devtools to see me being fetched from the server.')]

@router.get('/thread-content', response_model=FastUI, response_model_exclude_none=True)
async def thread_view() -> list[AnyComponent]:
    client=OpenAI()
    # Check if a thread ID already exists in the indatabase
    existing_thread_id = await db.get_thread_id()
    # Assuming 'main_thread' is a unique identifier for our main thread

    if existing_thread_id is None:
        # If a thread ID does not exist, create a new thread
        thread = client.beta.threads.create()

        # Store the new thread ID in the database
        new_thread = await db.create_thread_id(thread.id)
        thread_id = new_thread.thread_id
        logger.info(f"New thread created with ID: {thread_id}")
        await db.count_thread_ids()
    else:
        # Use the existing thread ID
        thread_id = existing_thread_id
        logger.info(f"Existing thread ID found: {thread_id}")

    thread_data=client.beta.threads.retrieve(thread_id=f'{thread_id}')
    messages = client.beta.threads.messages.list(thread_id=f'thread_XyBIO891EOEdlfEASAgm66zv')
    output_text = ""
    for message in messages.data:
            if message.role == "assistant":  # Filter messages by the assistant role
                for content_piece in message.content:
                    if content_piece.type == "text":
                        output_text += f"{content_piece.text.value}\n"
#create and add message to empty thread

    return [
        c.Paragraph(text=f'{thread_data}'),
        c.Paragraph(text=f'{output_text}')
            ]
